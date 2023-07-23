from .constants import DESTINATION_URL, SENSITIVE_HEADERS
from .transport import HTTPTransport


class Client(object):
    def __init__(
            self,
            api_key,
            *args,
            **kwargs
    ):
        self._api_key = api_key
        self._dest = DESTINATION_URL
        self._exclude_url_paths = kwargs.get('exclude_url_paths', [])
        self._exclude_urls_regex = kwargs.get('exclude_urls_regex', [])
        self._exclude_functions = kwargs.get('exclude_functions', [])
        self._exclude_sensitive_headers = kwargs.get('exclude_sensitive_headers', SENSITIVE_HEADERS)
        self._transport = HTTPTransport(self._api_key, self._dest)

    @property
    def transport(self):
        if self._transport is not None:
            return self._transport
