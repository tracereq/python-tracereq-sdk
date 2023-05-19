import uuid
from datetime import datetime
from collections.abc import Mapping
from .constants import HEADER_NAME, REQUEST, RESPONSE

class EnvironHeaders(Mapping):
    def __init__(self, environ, prefix="HTTP_"):
        self.environ = environ
        self.prefix = prefix

    def __getitem__(self, item):
        return self.environ[self.prefix + item.replace("-", "_").upper()]

    def __len__(self):
        return sum(1 for i in iter(self))

    def __int__(self):
        for key in self.environ:
            if not isinstance(key, str):
                continue

            key = key.replace("-", "_").upper()
            if not key.startswith(self.prefix):
                continue

            yield key[len(self.prefix):]


class Trace(object):
    def __init__(self):
        self.trace_id = None

    @classmethod
    def get_trace_from_headers(cls, environ):
        trace_id = EnvironHeaders(environ).get(HEADER_NAME)
        if trace_id is not None:
            trace_id = str(uuid.uuid4())

        return trace_id

def generate_trace_req_packet(trace_id, request):
    if not trace_id:
        return

    packet = {
        'type': REQUEST,
        'trace_id': trace_id,
        'host': request.host,
        'request_path': request.path,
        'request_full_path': request.full_path,
        'function_name': request.endpoint,
        'timestamp': datetime.now(),
        'headers': dict(request.headers),
        'remote_addr': request.remote_addr,
        'cookies': request.cookies if request.cookies else None,
        'data': request.data if request.data else None,
        'args': request.args if request.args else None,
    }

    return packet


def generate_trace_res_packet(trace_id, response):
    if not trace_id:
        return

    packet = {
        'type': RESPONSE,
        'timestamp': datetime.now(),
        'trace_id': trace_id,
        'headers': dict(response.headers),
        'code': response.code,
        'reason': response.reason,
        'status': response.status
    }

    return packet
