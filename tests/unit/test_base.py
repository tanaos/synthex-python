import responses
import pytest

from synthex import Synthex
from synthex.consts import API_BASE_URL, PING_ENDPOINT


@responses.activate
@pytest.mark.unit
def test_ping_success(synthex: Synthex):
    """
    Test the ping method of the Synthex class to ensure it successfully returns `True` when the 
    API responds with a 200 status code and a success message.
    Args:
        synthex (Synthex): An instance of the Synthex class to be tested.
    Assertions:
        - Asserts that the ping method returns True when the API 
          endpoint responds with a 200 status code and a success message.
    """
    
    responses.add(
        responses.GET,
        f"{API_BASE_URL}{PING_ENDPOINT}",
        json={"message": "Success"},
        status=200
    )
    
    assert synthex.ping() is True
    

@responses.activate
@pytest.mark.unit
def test_ping_failure(synthex: Synthex):
    """
    Test case for the ping method of the Synthex class to verify its behavior when the API 
    responds with a failure.
    Assertions:
        - The ping method should return False when the API responds with a 500 status code.
    """
    
    responses.add(
        responses.GET,
        f"{API_BASE_URL}{PING_ENDPOINT}",
        json={"message": "Failure"},
        status=500
    )
    
    assert synthex.ping() is False