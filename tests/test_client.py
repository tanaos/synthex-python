import responses
#import pytest

from synthex.client import APIClient
from synthex.config import config


@responses.activate
def test_ping_success(api_client: APIClient):
    responses.add(
        responses.GET,
        f"{config.API_BASE_URL}/",
        json={"message": "Success"},
        status=200
    )
    
    assert api_client.ping() is True