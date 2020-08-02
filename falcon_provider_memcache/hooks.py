# -*- coding: utf-8 -*-
"""Falcon memcache hook module."""
# standard library
from typing import Optional, Union

# third-party
import falcon

from .utils import MemcacheClient


def memcache_client(
    req: falcon.Request,
    resp: falcon.Response,
    resource: object,
    params: dict,
    server: Optional[Union[str, tuple]] = None,
    **kwargs
):  # pylint: disable=unused-argument
    """Provide an instance of memcache client to method via resource.

    .. note:: MemcacheClient is a singleton instance and therefore only needs the connection
        parameters provided once. It would be a best practice to establish the instance prior to
        using the hook so that the connection parameters are not required in the setup of the hook.

    .. code-block:: python
        :linenos:
        :lineno-start: 1

        @falcon.before(memcache_client)
        def on_get(self, req, resp):
            try:
                data = self.memcache_client.get('foo')
            except ConnectionRefusedError:
                raise falcon.HTTPInternalServerError(
                    code=self.code(),
                    description='Unexpected error occurred while retrieving data.',
                    title='Internal Server Error',
                )

    Args:
        req: The falcon req object.
        resp: The falcon resp object.
        resource: The falcon resp object.
        params: List of query params.
        server: The server settings for memcache, can either be a
            (host, port) tuple for a TCP connection or a string containing the path to a
            UNIX domain socket.
    """
    resource.memcache_client = MemcacheClient(server, **kwargs).client
