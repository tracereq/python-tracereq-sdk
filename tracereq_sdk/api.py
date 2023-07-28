from .engine import Engine
from .client import Client
from .integrations import setup_integrations

__all__ = ['Engine', 'Client']


def public(f):
    __all__.append(f.__name__)
    return f


@public
def init(api_key, *args, **kwargs):
    client = Client(api_key, *args, **kwargs)
    Engine.main.attach_client(client)
    setup_integrations(*args, **kwargs)

