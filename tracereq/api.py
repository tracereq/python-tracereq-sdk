from .hub import Hub
from .client import Client
from . import setup_integrations

__all__ = ['Hub', 'Client']

def public(f):
    __all__.append(f.__name__)
    return f

@public
def init(flask_wsgi_app, *args, **kwargs):
    client = Client(*args, **kwargs)
    Hub.master.attach_client(client)
    setup_integrations(flask_wsgi_app)
