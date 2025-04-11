import responses
import pytest

from synthex import Synthex
from synthex.endpoints import API_BASE_URL, GET_PROMOTIONAL_CREDITS_ENDPOINT
from synthex.models import CreditModel
from synthex.exceptions import NotFoundError, AuthenticationError


@pytest.mark.unit
@responses.activate
def test_promotional_success(synthex: Synthex):
    """
    This test verifies that the `promotional` method of the `credits` module
    in the `Synthex` class correctly retrieves promotional credit information
    from the API and maps it to a `CreditModel` instance.
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
     
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/{GET_PROMOTIONAL_CREDITS_ENDPOINT}",
        json={
            "status_code": 200,
            "status": "success",
            "message": "Credits retrieved successfully",
            "data": {
                "amount": 100,
                "currency": "USD",
            }
        },
        status=200
    )

    credits_info = synthex.credits.promotional()

    assert isinstance(credits_info, CreditModel), "Promotional credits info is not of type CreditModel."
    assert credits_info.amount== 100, "Promotional credits amount is not 100."
    assert credits_info.currency == "USD", "Promotional credits currency is not USD."
    

@pytest.mark.unit 
@responses.activate
def test_promotional_401_failure(synthex: Synthex):
    """
    Test case for verifying the behavior of the `promotional` method when the API
    responds with a 401 Unauthorized error.
    This test simulates an unauthorized API response by mocking the GET request
    to the promotional credits endpoint. It ensures that the `promotional` method
    raises an `AuthenticationError` when the API returns a 401 status code.
    Args:
        synthex (Synthex): An instance of the Synthex class to test.
    """
    
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/{GET_PROMOTIONAL_CREDITS_ENDPOINT}",
        json={"error": "unauthorized"},
        status=401
    )

    try:
        with pytest.raises(AuthenticationError):
            synthex.credits.promotional()
    except AssertionError:
        pytest.fail("Expected AuthenticationError to be raised, but it wasn't.")


@pytest.mark.unit
@responses.activate
def test_promotional_404_failure(synthex: Synthex):
    """
    Test case for handling a 404 Not Found error when attempting to retrieve
    promotional credits.
    This test simulates a scenario where the API endpoint for fetching
    promotional credits returns a 404 status code. It verifies that the
    `synthex.credits.promotional()` method raises a `NotFoundError` exception
    in response to the error.
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
    
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/{GET_PROMOTIONAL_CREDITS_ENDPOINT}",
        json={
            "status_code": 404,
            "status": "error",
            "message": "Not found",
            "details": None
        },
        status=404
    )

    try:
        with pytest.raises(NotFoundError):
            synthex.credits.promotional()
    except AssertionError:
        pytest.fail("Expected NotFoundError to be raised, but it wasn't.")