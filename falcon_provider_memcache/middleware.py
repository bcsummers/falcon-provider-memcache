"""Falcon memcache middleware module."""

# third-party
import falcon

from .utils import MemcacheClient


class MemcacheMiddleware:
    """Memcache middleware module.

    For a full list of kwargs see:

    https://pymemcache.readthedocs.io/en/latest/apidoc/pymemcache.client.base.html#pymemcache.client.base.Client

    Args:
        server: The server settings for memcache, can either be a (host, port) tuple for
            a TCP connection or a string containing the path to a UNIX domain socket.
        cache_memlimit (int, kwargs): The number of megabytes to set as the new cache memory limit.
        connect_timeout (int, kwargs): Used to set socket timeout values. By default, timeouts
            are disabled.
        deserializer (callable, kwargs): The deserialization function takes three
            parameters, a key, value and flags and returns the deserialized value.
        no_delay (bool, kwargs): Sets TCP_NODELAY socket option.
        serializer (callable, kwargs): The serialization function takes two arguments,
            a key and a value, and returns a tuple of two elements, the serialized value, and an
            integer in the range 0-65535 (the "flags").
        timeout (int, kwargs): Used to set socket timeout values. By default, timeouts are
            disabled.
    """

    def __init__(self, server: str | tuple | None = None, **kwargs):
        """Initialize class properties."""
        server = server or ('localhost', 11211)
        self.memcache_client = MemcacheClient(server, **kwargs).client

    # pylint: disable=unused-argument
    def process_resource(
        self, req: falcon.Request, resp: falcon.Response, resource: object, params: dict
    ):
        """Process resource method.

        .. code-block:: python
            :linenos:
            :lineno-start: 1

            def on_get(self, req, resp):
                try:
                    data = self.memcache_client.get('foo')
                except ConnectionRefusedError:
                    raise falcon.HTTPInternalServerError(
                        code=self.code(),
                        description='Unexpected error occurred while retrieving data.',
                        title='Internal Server Error',
                    )
        """
        resource.memcache_client = self.memcache_client
