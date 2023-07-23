import json
import urllib3
from .constants import TRANSPORT_SEND_TIMEOUT
from datetime import datetime, date


class TraceEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if isinstance(o, bytes):
            return o.decode('utf-8', errors='ignore')

        output = repr(o)
        try:
            output = json.JSONEncoder.default(self, o)
        except TypeError:
            pass
        return output


def to_json(obj):
    return json.dumps(obj, cls=TraceEncoder, ensure_ascii=True)


class HTTPTransport(object):
    def __init__(self, api_key, dest):
        self.api_key = api_key
        self.dest = dest
        self.timeout = TRANSPORT_SEND_TIMEOUT
        self.session = urllib3.PoolManager(
            headers={
                'Authorization': 'Bearer {}'.format(self.api_key),
                'Content-Type': 'application/json'
            },
            maxsize=5
        )

    def send(self, trace_doc):
        try:
            trace_doc['timestamp'] = datetime.utcnow()
            self.session.request(
                'POST',
                self.dest,
                body=to_json(trace_doc),
                timeout=self.timeout,
                retries=False
            )
        except Exception as ex:
            pass
