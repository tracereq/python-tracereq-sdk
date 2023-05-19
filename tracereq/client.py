from .constants import DESTINATION_URL
from .transport import HTTPTransport

class Client(object):
    def __init__(
            self,
            token: str = '',
            dest: str = DESTINATION_URL,
            *args,
            **kwargs
    ):
        self._token = token
        self._dest = dest
        self._transport = HTTPTransport(self._token, self._dest)

    @property
    def transport(self):
        if self._transport is not None:
            return self._transport
