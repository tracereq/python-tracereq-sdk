from threading import local

_local = local()


class Hub():
    current = None

    def __init__(self, client_or_hub=None):
        if isinstance(client_or_hub, Hub):
            hub = client_or_hub
            client = hub._client
        else:
            client = client_or_hub

        self._client = client
        self._trace = None

    def set_trace(self, trace):
        self._trace = trace

    def get_trace(self):
        return self._trace

    @property
    def client(self):
        return self._client

    def attach_client(self, client):
        self._client = client
