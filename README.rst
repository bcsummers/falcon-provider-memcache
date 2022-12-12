========================
falcon-provider-memcache
========================

|build| |coverage| |code-style| |pre-commit|

A falcon hook and middleware provider for memcache.

------------
Installation
------------

Install the extension via pip.

.. code:: bash

    > pip install falcon-provider-memcache

--------
Overview
--------

This package provides a hook and middleware component for the falcon framework via the MemcacheClient class in utils.py. This class is a Singleton that uses a connection pool for the memcache client.  The MemcacheClient class can also be accessed directly outside of the hook or middleware if required.  There is also a stand-alone ``memcache_client`` method that provides a single client connection to memcached.

--------
Requires
--------
* Falcon - https://pypi.org/project/falcon/
* pymemcache - https://pypi.org/project/pymemcache/

----
Hook
----

The memcache_client hook can be applied at the class level or the method level. If applied at the class level each responder method will have access to ``self.memcache_client`` (an instance of pymemcache.client.base.PooledClient) or if applied at the method level that method will have access to ``self.memcache_client``. For more information on falcon hooks see https://falcon.readthedocs.io/en/stable/api/hooks.html and for more information on memcache client methods see https://pymemcache.readthedocs.io/en/latest/apidoc/pymemcache.client.base.html#pymemcache.client.base.PooledClient.

.. code:: python

    import os
    import falcon
    from falcon_provider_memcache.hooks import memcache_client

    # Memcached
    MEMCACHE_HOST = os.getenv('MEMCACHE_HOST', 'localhost')
    MEMCACHE_PORT = int(os.getenv('MEMCACHE_PORT', '11211'))

    class MemcacheHookResource(object):
        """Memcache hook testing resource."""

        @falcon.before(memcache_client, server=(MEMCACHE_HOST, MEMCACHE_PORT))
        def on_get(self, req, resp):
            key = req.get_params('key')
            try:
                data = self.memcache_client.get(key)
            except ConnectionRefusedError:
                raise falcon.HTTPInternalServerError(
                    code=self.code(),
                    description='Unexpected error occurred while retrieving data.',
                    title='Internal Server Error',
                )

    app_middleware = falcon.App()
    app_middleware.add_route('/hook', MemcacheHookResource()

----------
Middleware
----------

When using MemcacheMiddleWare all responder methods will have access to ``self.memcache_client`` (an instance of pymemcache.client.base.PooledClient). For more information on falcon hooks see https://falcon.readthedocs.io/en/stable/api/hooks.html and for more information on memcache client methods see https://pymemcache.readthedocs.io/en/latest/apidoc/pymemcache.client.base.html#pymemcache.client.base.PooledClient.

.. code:: python

    import os
    import falcon
    from falcon_provider_memcache.middleware import MemcacheMiddleware

    # Memcached
    MEMCACHE_HOST = os.getenv('MEMCACHE_HOST', 'localhost')
    MEMCACHE_PORT = int(os.getenv('MEMCACHE_PORT', '11211'))

    class MemcacheMiddleWareResource(object):
        """Memcache middleware testing resource."""

        def on_get(self, req, resp):
            """Support GET method."""
            key = req.get_param('key')
            try:
                resp.text = self.memcache_client.get(key)
                resp.status_code = falcon.HTTP_OK
            except ConnectionRefusedError:
                raise falcon.HTTPInternalServerError(
                    code=1234,
                    description='Unexpected error occurred while retrieving data.',
                    title='Internal Server Error',
                )

    app_middleware = falcon.App(middleware=[MemcacheMiddleware(server=(MEMCACHE_HOST, MEMCACHE_PORT))])
    app_middleware.add_route('/middleware', MemcacheMiddleWareResource()

-----------
Development
-----------

Installation
------------

After cloning the repository, all development requirements can be installed via pip. For linting and code consistency the pre-commit hooks should be installed.

.. code:: bash

    > poetry install --with dev
    > pre-commit install

Testing
-------

.. code:: bash

    > poetry install --with dev,test
    > pytest --cov=falcon_provider_memcache --cov-report=term-missing tests/

.. |build| image:: https://github.com/bcsummers/falcon-provider-memcache/workflows/build/badge.svg
    :target: https://github.com/bcsummers/falcon-provider-memcache/actions

.. |coverage| image:: https://codecov.io/gh/bcsummers/falcon-provider-memcache/branch/master/graph/badge.svg?token=UHAZvGDApk
    :target: https://codecov.io/gh/bcsummers/falcon-provider-memcache

.. |code-style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit
    :alt: pre-commit
