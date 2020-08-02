# -*- coding: utf-8 -*-
"""Falcon app used for testing."""
# standard library
import os

# third-party
import falcon

# first-party
from falcon_provider_memcache.hooks import memcache_client
from falcon_provider_memcache.middleware import MemcacheMiddleware

# Memcached
MEMCACHE_HOST = os.getenv('MEMCACHE_HOST', 'localhost')
MEMCACHE_PORT = int(os.getenv('MEMCACHE_PORT', '11211'))


class MemcacheHookResource:
    """Memcache hook testing resource."""

    @falcon.before(memcache_client, server=(MEMCACHE_HOST, MEMCACHE_PORT))
    def on_get(
        self, req: falcon.Request, resp: falcon.Response,
    ):
        """Support GET method."""
        key: str = req.get_param('key')
        try:
            resp.body = self.memcache_client.get(key)  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except ConnectionRefusedError:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            )

    @falcon.before(memcache_client, server=(MEMCACHE_HOST, MEMCACHE_PORT))
    def on_post(
        self, req: falcon.Request, resp: falcon.Response,
    ):
        """Support POST method."""
        key: str = req.get_param('key')
        value: str = req.get_param('value')
        try:
            resp.body = str(self.memcache_client.set(key, value))  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except ConnectionRefusedError:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            )


app_hook = falcon.API()
app_hook.add_route('/hook', MemcacheHookResource())


class MemcacheMiddleWareResource:
    """Memcache middleware testing resource."""

    def on_get(
        self, req: falcon.Request, resp: falcon.Response,
    ):
        """Support GET method."""
        key = req.get_param('key')
        try:
            resp.body = self.memcache_client.get(key)  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except ConnectionRefusedError:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            )

    def on_post(
        self, req: falcon.Request, resp: falcon.Response,
    ):
        """Support POST method."""
        key: str = req.get_param('key')
        value: str = req.get_param('value')
        try:
            resp.body = str(self.memcache_client.set(key, value))  # pylint: disable=no-member
            resp.status_code = falcon.HTTP_OK
        except ConnectionRefusedError:
            raise falcon.HTTPInternalServerError(
                code=1234,
                description='Unexpected error occurred while retrieving data.',
                title='Internal Server Error',
            )


app_middleware = falcon.API(middleware=[MemcacheMiddleware(server=(MEMCACHE_HOST, MEMCACHE_PORT))])
app_middleware.add_route('/middleware', MemcacheMiddleWareResource())
