from threading import local

_local = local()


class ParentEngine(type):
    @property
    def current(cls):
        try:
            existing_engine = _local.engine
        except AttributeError:
            _local.engine = existing_engine = Engine(MAIN_ENGINE)
        return existing_engine

    @property
    def main(cls):
        return MAIN_ENGINE


def with_metaclass(meta, *bases):
    class metaclass(type):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(metaclass, "temporary_class", (), {})


class Engine(with_metaclass(ParentEngine)):
    def __init__(self, _engine=None):
        if isinstance(_engine, Engine):
            engine = _engine
            client = engine._client
        else:
            client = _engine

        self._client = client
        self._trace = None
        self._request_in_process = None

    def set_trace(self, trace):
        self._trace = trace

    def get_trace(self):
        return self._trace

    def set_request_data(self, request_data):
        self._request_in_process = request_data

    def get_request_data(self):
        return self._request_in_process

    @property
    def client(self):
        return self._client

    def attach_client(self, client):
        self._client = client


MAIN_ENGINE = Engine()
_local.engine = MAIN_ENGINE
