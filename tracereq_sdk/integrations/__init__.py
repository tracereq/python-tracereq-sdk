from threading import Lock

_installer_lock = Lock()
_installed_integrations = {}


def get_core_integrations():
    from tracereq_sdk.customlib import CustomlibIntegration
    yield CustomlibIntegration()


def get_custom_integrations(**kwargs):
    if kwargs.get('flask_app'):
        from .flasklib import FlasklibIntegration
        yield FlasklibIntegration(kwargs.get('flask_app'))


def setup_integrations(*args, **kwargs):
    integrations = list()

    core_integrations = get_core_integrations()
    custom_integrations = get_custom_integrations(**kwargs)
    for instance in core_integrations:
        if not any(isinstance(x, type(instance)) for x in integrations):
            integrations.append(instance)

    for instance in custom_integrations:
        if not any(isinstance(x, type(instance)) for x in integrations):
            integrations.append(instance)

    for integration in integrations:
        integration()


class Integration(object):
    integration_key = None

    def install(self):
        raise NotImplementedError()

    def __call__(self, environ=None, start_response=None):
        assert self.integration_key
        with _installer_lock:
            if self.integration_key in _installed_integrations:
                return

            self.install()
            _installed_integrations[self.integration_key] = self
