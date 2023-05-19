from . import Integration
from .hub import Hub
from .constants import HEADER_NAME, DESTINATION_URL
from .tracing import generate_trace_res_packet


try:
    from httplib import HTTPConnection
except ImportError:
    from http.client import HTTPConnection


class CustomlibIntegration(Integration):
    identifier = "customlib"

    def __init__(self):
        self.custom_httplib_connection = HTTPConnection

    def install_httplib(self):
        original_putrequest = self.custom_httplib_connection.putrequest
        original_getresponse = self.custom_httplib_connection.getresponse

        def custom_putrequest(self, method, url, *args, **kwargs):
            self.hub = Hub.current
            req = original_putrequest(self, method, url, *args, **kwargs)
            if DESTINATION_URL in self.host or self.port == 8003:
                return req

            self._trace_id = self.hub.get_trace()
            if self._trace_id:
                self.putheader(HEADER_NAME, self._trace_id)
                print('outgoing -> {}'.format(self._trace_id))

            return req

        def custom_getresponse(self, *args, **kwargs):
            res = original_getresponse(self, *args, **kwargs)
            if DESTINATION_URL in self.host or self.port == 8003:
                return res

            trace_id = self._trace_id
            current_res_packet = generate_trace_res_packet(trace_id, res)
            self.hub.client.transport.send(current_res_packet)
            return res

        HTTPConnection.putrequest = custom_putrequest
        HTTPConnection.getresponse = custom_getresponse

    def install(self):
        self.install_httplib()
 
