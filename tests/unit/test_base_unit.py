import responses
import pytest

from synthex import Synthex
from synthex.endpoints import API_BASE_URL, PING_ENDPOINT


@responses.activate
@pytest.mark.unit
def test_ping_success(synthex: Synthex):
    """
    Test the `ping` method of the `Synthex` class to ensure it successfully
    returns `True` when the API responds with a 200 status and a success message.
    Steps:
    1. Mock the API response for the ping endpoint with a 200 status and a JSON
        payload containing a success message.
    2. Call the `ping` method of the `Synthex` instance.
    3. Assert that the method returns `True` indicating a successful ping.
    Assertions:
        - The ping method should return True when the API responds with a 200 status code.
    Args:
        synthex (Synthex): An instance of the Synthex class to test.
    """
    
    responses.add(
        responses.GET,
        f"{API_BASE_URL}{PING_ENDPOINT}",
        json={"message": "Success"},
        status=200
    )
    
    assert synthex.ping() is True, "Ping failed, Synthex instance is not functioning as expected."
    

@responses.activate
@pytest.mark.unit
def test_ping_failure(synthex: Synthex):
    """
    Test the `ping` method of the `Synthex` class to ensure it handles failure scenarios correctly.
    This test simulates a server failure by mocking a 500 Internal Server Error response
    from the `PING_ENDPOINT`. It verifies that the `ping` method returns `False` when
    the server is unreachable or returns an error status.
    Args:
        synthex (Synthex): An instance of the `Synthex` class to be tested.
    Setup:
        - Mock the HTTP GET request to the `PING_ENDPOINT` using the `responses` library.
        - Configure the mock to return a 500 status code with a failure message.
    """
    
    responses.add(
        responses.GET,
        f"{API_BASE_URL}{PING_ENDPOINT}",
        json={"message": "Failure"},
        status=500
    )
    
    assert synthex.ping() is False, "Ping should fail, but it returned True."