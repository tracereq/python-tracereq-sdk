import uuid
import re
from datetime import datetime
from .constants import HEADER_NAME


trace_header_regex = re.compile(
    "^[ \t]*([0-9a-f]{32})-([0-9a-f]{16})" "(-.*)?[ \t]*$"
)


class EnvironHeaders(object):
    def __init__(self, environ):
        self.environ = environ

    def get(self, key):
        return self.environ.get("HTTP_" + key.replace("-", "_").upper())


class Trace(object):
    def __init__(self, trace_id, span_id, span_type=None, parent_span_id=None, start_timestamp=None):
        self.trace_id = trace_id
        self.span_id = span_id
        self.span_type = span_type
        self.parent_span_id = parent_span_id
        self.start_timestamp = start_timestamp or datetime.utcnow()
        self.end_timestamp = None
        self.data = {}

    @staticmethod
    def init_new_trace_id():
        return uuid.uuid4().hex

    @staticmethod
    def init_new_span_id():
        return uuid.uuid4().hex[16:]

    def start_new_span(self, span_type=None):
        parent_span_id = self.span_id or None

        if self.trace_id is None:
            return Trace.begin_trace()
        return Trace(
            trace_id=self.trace_id,
            span_id=self.init_new_span_id(),
            parent_span_id=parent_span_id,
            span_type=span_type
        )

    @staticmethod
    def mark_finish(trace_or_span):
        trace_or_span.end_timestamp = datetime.utcnow()

    @staticmethod
    def set_span_data(span, key, value):
        span.data[key] = value

    @classmethod
    def begin_trace(cls, span_type=None):
        return cls(
            trace_id=cls.init_new_trace_id(), span_id=cls.init_new_span_id(), span_type=span_type
        )

    @classmethod
    def get_trace_from_environ(cls, environ, span_type=None):
        return cls.get_trace_from_headers(EnvironHeaders(environ), span_type)

    @classmethod
    def get_trace_from_headers(cls, headers, span_type=None):
        parent_span = cls.deconstruct_trace_header_info(headers.get(HEADER_NAME))
        if parent_span is None:
            return cls.begin_trace(span_type)

        return parent_span.start_new_span(span_type)

    @classmethod
    def deconstruct_trace_header_info(cls, trace_header):
        if not trace_header:
            return None

        regex_matches = trace_header_regex.match(trace_header)
        if regex_matches is None:
            return None

        trace_id, span_id, meta_info = regex_matches.groups()
        return cls(trace_id=trace_id, span_id=span_id)

    def construct_trace_header_info(self):
        return '{}-{}'.format(self.trace_id, self.span_id)

    def to_json(self):
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "span_type": self.span_type,
            "parent_span_id": self.parent_span_id,
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "data": self.data,
        }

    @staticmethod
    def get_trace_id_from_trace_object(trace_object):
        return trace_object.trace_id


def generalize_request(request):
    data = {
        'host': request.host,
        'request_path': request.path,
        'request_full_path': request.full_path,
        'function_name': request.endpoint,
        'headers': dict(request.headers),
        'remote_addr': request.remote_addr,
        'method': request.method,
        'cookies': request.cookies if request.cookies else None,
        'data': request.data if request.data else None,
        'args': request.args if request.args else None,
    }

    return data


def generate_trace_event(trace, request_data, response_data):
    if not trace:
        return

    span_event = {
        'span_type': trace.span_type,
        'trace_id': trace.trace_id,
        'span_id': trace.span_id,
        'start_timestamp': trace.start_timestamp,
        'end_timestamp': trace.end_timestamp or None,
        'function_name': request_data.get('function_name'),
        'http.host': request_data.get('host'),
        'http.path': request_data.get('request_path'),
        'http.method': request_data.get('method', None),
        'http.full_path': request_data.get('request_full_path'),
        'http.headers': dict(request_data.get('headers')),
        'http.remote_addr': request_data.get('remote_addr'),
        'http.cookies': request_data.get('cookies', None),
        'http.data': request_data.get('data', None),
        'http.args': request_data.get('args', None),
        'response_data': response_data.get_data().decode("utf-8"),
        'status_code': response_data.status_code
    }

    return span_event
