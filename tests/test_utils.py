# -*- coding: utf-8 -*-
"""Test hooks feature of falcon_provider_memcache module."""
# standard library
import os

# first-party
from falcon_provider_memcache.utils import memcache_client

# Memcached
MEMCACHE_HOST = os.getenv('MEMCACHE_HOST', 'localhost')
MEMCACHE_PORT = int(os.getenv('MEMCACHE_PORT', '11211'))


def test_utils_memcache_client() -> None:
    """Testing utils stand-alone memcache_client method"""
    client = memcache_client(server=(MEMCACHE_HOST, MEMCACHE_PORT))
    key = 'utils_test_key'
    value = 'utils_test_value'
    result = client.set(key, value)
    assert result is True

    data = client.get(key)
    assert data.decode() == value
