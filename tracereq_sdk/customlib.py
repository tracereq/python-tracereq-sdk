from .integrations import Integration
from .engine import Engine
from .constants import HEADER_NAME, DESTINATION_URL
from urllib.parse import urlsplit


try:
    from httplib import HTTPConnection
except ImportError:
    from http.client import HTTPConnection


class CustomlibIntegration(Integration):
    integration_key = "customlib"

    def __init__(self):
        self.custom_httplib_connection = HTTPConnection

    def install_httplib(self):
        original_putrequest = self.custom_httplib_connection.putrequest
        original_getresponse = self.custom_httplib_connection.getresponse

        def custom_putrequest(self, method, url, *args, **kwargs):
            self.engine = Engine.current
            req = original_putrequest(self, method, url, *args, **kwargs)
            if self.host in DESTINATION_URL:
                return req

            parsed_url = urlsplit(url)

            self._trace = self.engine.get_trace()

            span = self._trace.start_new_span(span_type='http.client')
            self._trace.set_span_data(span, 'http.method', method)
            self._trace.set_span_data(span, 'http.path', parsed_url.path)
            self._trace.set_span_data(span, 'http.query', parsed_url.query)

            if self._trace:
                self.putheader(HEADER_NAME, span.construct_trace_header_info())

            self._span = span
            return req

        def custom_getresponse(self, *args, **kwargs):
            res = original_getresponse(self, *args, **kwargs)
            if self.host in DESTINATION_URL:
                return res

            self._trace = self.engine.get_trace()

            current_span_event = self._span
            self._trace.mark_finish(current_span_event)
            self._trace.set_span_data(current_span_event, 'reason', res.reason)
            self._trace.set_span_data(current_span_event, 'status_code', res.status)

            self.engine.client.transport.send(current_span_event.to_json())
            return res

        HTTPConnection.putrequest = custom_putrequest
        HTTPConnection.getresponse = custom_getresponse

    def install(self):
        self.install_httplib()
