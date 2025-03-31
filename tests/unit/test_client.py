import responses
import pytest

from synthex.client import APIClient
from synthex.config import config
from synthex.consts import PING_ENDPOINT


@responses.activate
@pytest.mark.unit
def test_ping_success(api_client: APIClient):
    """
    Test the ping method of the APIClient to ensure it successfully returns `True` when the 
    API responds with a 200 status code and a success message.
    Args:
        api_client (APIClient): An instance of the APIClient to be tested.
    Assertions:
        - Asserts that the ping method returns True when the API 
          endpoint responds with a 200 status code and a success message.
    """
    
    responses.add(
        responses.GET,
        f"{config.API_BASE_URL}{PING_ENDPOINT}",
        json={"message": "Success"},
        status=200
    )
    
    assert api_client.ping() is True
    

@responses.activate
@pytest.mark.unit
def test_ping_failure(api_client: APIClient):
    """
    Test case for the ping method of the APIClient class to verify its behavior when the API 
    responds with a failure.
    Assertions:
        - The ping method should return False when the API responds with a 500 status code.
    """
    
    responses.add(
        responses.GET,
        f"{config.API_BASE_URL}{PING_ENDPOINT}",
        json={"message": "Failure"},
        status=500
    )
    
    assert api_client.ping() is False