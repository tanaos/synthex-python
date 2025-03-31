import pytest

from synthex.client import APIClient


@pytest.mark.integration
def test_ping(api_client: APIClient):
    assert api_client.ping() is True