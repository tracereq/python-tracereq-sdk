from threading import Lock

_installer_lock = Lock()
_installed_integrations = {}

def get_default_integrations(wsgi_app):
    from .customhttplib import CustomHttpLib
    yield CustomHttpLib()

    from .flasklib import FlaskLib
    yield FlaskLib(wsgi_app)


def setup_integrations(wsgi_app):
    integrations = list()
    for integration in get_default_integrations(wsgi_app):
        if not any(isinstance(x, type(integration)) for x in integrations):
            integrations.append(integration)

    for integration in integrations:
        integration()


class Integration(object):
    identifier = None

    def install(self):
        raise NotImplementedError()

    def __call__(self, environ=None, start_response=None):
        assert self.identifier
        with _installer_lock:
            if self.identifier in _installed_integrations:
                return

            self.install()
            _installed_integrations[self.identifier] = self
