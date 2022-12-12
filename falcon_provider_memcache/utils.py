"""Memcache client utility."""

# third-party
import pymemcache


class Singleton(type):
    """A singleton Metaclass"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Evoke call method."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# Using Pool over standard client as default
# class MemcacheClient(metaclass=Singleton):
#     """A shared memcache client connection singleton.
#
#     For a full list of kwargs see:
#
#     https://pymemcache.readthedocs.io/en/latest/apidoc/pymemcache.client.base.html
#     #pymemcache.client.base.Client
#
#     Args:
#         server (str; tuple, optional): The server settings for memcache, can either be a
#             (host, port) tuple for a TCP connection or a string containing the path to a
#             UNIX domain socket.
#         cache_memlimit (int): the number of megabytes to set as the new cache memory limit.
#         connect_timeout (int, kwargs): Used to set socket timeout values. By default, timeouts are
#             disabled.
#         deserializer (function or method, kwargs): The deserialization function takes three
#             parameters, a key, value and flags and returns the deserialized value.
#         no_delay (book, kwargs): Sets TCP_NODELAY socket option.
#         serializer (function or method, kwargs): The serialization function takes two arguments, a
#             key and a value, and returns a tuple of two elements, the serialized value, and an
#             integer in the range 0-65535 (the “flags”).
#         timeout (int, kwargs): Used to set socket timeout values. By default, timeouts are
#             disabled.
#     """
#
#     def __init__(self, server=None, cache_memlimit=50, **kwargs):
#         """Initialize class properties"""
#         server = server or ('localhost', 11211)
#
#         self._client = pymemcache.client.base.Client(server)
#         self._client.cache_memlimit(cache_memlimit)
#
#     @property
#     def client(self):
#         """Return an instance of pymemcache.client.base.Client."""
#         return self._client


class MemcacheClient(metaclass=Singleton):
    """A shared memcache client pool connection singleton.

    For a full list of kwargs see:

    https://pymemcache.readthedocs.io/en/latest/apidoc/pymemcache.client.base.html#pymemcache.client.base.PooledClient

    Args:
        server: The server settings for memcache, can either be a (host, port) tuple for
            a TCP connection or a string containing the path to a UNIX domain socket.
        max_pool_size: The maximum pool size for Pool Client.
        connect_timeout (int, kwargs): Used to set socket timeout values. By default, timeouts are
            disabled.
        deserializer (callable, kwargs): The deserialization function takes three
            parameters, a key, value and flags and returns the deserialized value.
        no_delay (bool, kwargs): Sets TCP_NODELAY socket option.
        serializer (callable, kwargs): The serialization function takes two arguments, a
            key and a value, and returns a tuple of two elements, the serialized value, and an
            integer in the range 0-65535 (the "flags").
        timeout (int, kwargs): Used to set socket timeout values. By default, timeouts are disabled.
    """

    def __init__(self, server: str | tuple = None, max_pool_size: int | None = None, **kwargs):
        """Initialize class properties"""
        server = server or ('localhost', 11211)

        self._client = pymemcache.client.base.PooledClient(
            server, max_pool_size=max_pool_size, **kwargs
        )

    @property
    def client(self):
        """Return an instance of pymemcache.client.base.Client."""
        return self._client


def memcache_client(server: str | tuple, **kwargs):
    """Return an instance of pymemcache.client.base.Client.

    For a full list of kwargs see:

    https://pymemcache.readthedocs.io/en/latest/apidoc/pymemcache.client.base.html#pymemcache.client.base.Client

    Args:
        server: The server settings for memcache, can either be a (host, port) tuple for
            a TCP connection or a string containing the path to a UNIX domain socket.
        cache_memlimit (int, kwargs): the number of megabytes to set as the new cache memory limit.
        connect_timeout (int, kwargs): Used to set socket timeout values. By default, timeouts are
            disabled.
        deserializer (callable, kwargs): The deserialization function takes three
            parameters, a key, value and flags and returns the deserialized value.
        no_delay (bool, kwargs): Sets TCP_NODELAY socket option.
        serializer (callable, kwargs): The serialization function takes two arguments, a
            key and a value, and returns a tuple of two elements, the serialized value, and an
            integer in the range 0-65535 (the "flags").
        timeout (int, kwargs): Used to set socket timeout values. By default, timeouts are disabled.
    """
    return pymemcache.client.base.Client(server, **kwargs)
