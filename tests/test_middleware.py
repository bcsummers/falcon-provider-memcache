"""Test hooks feature of falcon_provider_memcache module."""

# third-party
from falcon.testing import Result


def test_middleware_post(client_middleware: object) -> None:
    """Testing GET resource

    Args:
        client_middleware (fixture): The test client.
    """
    params = {'key': 'middleware', 'value': 'middleware-worked'}
    response: Result = client_middleware.simulate_post('/middleware', params=params)
    # TODO: assert format for dates
    assert response.text == 'True'
    assert response.status_code == 200


def test_middleware_get(client_middleware: object) -> None:
    """Testing GET resource

    Args:
        client_middleware (fixture): The test client.
    """
    params = {'key': 'middleware'}
    response: Result = client_middleware.simulate_get('/middleware', params=params)
    assert response.text == 'middleware-worked'
    assert response.status_code == 200
