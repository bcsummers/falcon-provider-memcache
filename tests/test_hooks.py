"""Test hooks feature of falcon_provider_memcache module."""

# third-party
from falcon.testing import Result


def test_hooks_post(client_hook: object):
    """Testing GET method

    Args:
        client_hook (fixture): The test client.
    """
    params = {'key': 'hook', 'value': 'hook-worked'}
    response: Result = client_hook.simulate_post('/hook', params=params)
    # TODO: assert format for dates
    assert response.text == 'True'
    assert response.status_code == 200


def test_hooks_get(client_hook):
    """Testing GET method

    Args:
        client_hook (fixture): The test client.
    """
    params = {'key': 'hook'}
    response: Result = client_hook.simulate_get('/hook', params=params)
    assert response.text == 'hook-worked'
    assert response.status_code == 200
