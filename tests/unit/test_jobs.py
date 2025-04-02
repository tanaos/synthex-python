import responses
import pytest
from datetime import datetime, timezone

from synthex import Synthex
from synthex.consts import API_BASE_URL, GET_CURRENT_USER_ENDPOINT
from synthex.models import UserResponseModel
from synthex.exceptions import NotFoundError, AuthenticationError


endpoint = f"{API_BASE_URL}/{GET_CURRENT_USER_ENDPOINT}"

@responses.activate
def test_me_success(synthex: Synthex, ):
    """
    Test the `me` method of the `users` module in the `Synthex` class.
    This test verifies that the `me` method correctly retrieves and parses
    the current user's information from the API response.
    Assertions:
    - The returned object is an instance of `UserResponseModel`.
    - The `id` field matches the expected value.
    - The `first_name` field matches the expected value.
    - The `last_name` field matches the expected value.
    - The `email` field matches the expected value.
    - The `default_payment_method_id` field matches the expected value.
    - The `promo_credit_granted` field matches the expected datetime value.
    - The `is_verified` field matches the expected boolean value.
    Steps:
    1. Mock an HTTP GET request to the endpoint with a successful response.
    2. Parse the response into a `UserResponseModel` object.
    3. Assert that the returned object has the expected attributes and values.
    Args:
        synthex (Synthex): An instance of the Synthex class to test.
    """
    
    responses.add(
        responses.GET,
        endpoint,
        json={
            "status_code": 200,
            "status": "success",
            "message": "User retrieved successfully",
            "data": {
                "id": "abc123",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@gmail.com",
                "default_payment_method_id": "def456",
                "promo_credit_granted": datetime(
                    2025, 3, 15, 18, 20, 41, 677278, tzinfo=timezone.utc
                ).isoformat(),
                "is_verified": True   
            }
        },
        status=200
    )

    user = synthex.users.me()

    assert isinstance(user, UserResponseModel)
    assert user.id == "abc123"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@gmail.com"
    assert user.default_payment_method_id == "def456"
    assert user.promo_credit_granted == datetime(2025, 3, 15, 18, 20, 41, 677278, tzinfo=timezone.utc)
    assert user.is_verified is True
    
    
@responses.activate
def test_me_401_failure(synthex: Synthex):
    """
    Test that the `me` method of the `users` module in the `Synthex` class
    raises an `AuthenticationError` when the API responds with a 401 
    Unauthorized error.
    Steps:
    1. Mock an HTTP GET request to the endpoint with a 401 status code and 
       an error message indicating unauthorized access.
    2. Assert that calling `synthex.users.me()` raises an `AuthenticationError`.
    Args:
        synthex (Synthex): An instance of the Synthex class to test.
    """
    
    responses.add(
        responses.GET,
        endpoint,
        json={"error": "unauthorized"},
        status=401
    )

    with pytest.raises(AuthenticationError):
        synthex.users.me()


@responses.activate
def test_me_404_failure(synthex: Synthex):
    """
    Test case for handling a 404 Not Found error when retrieving the current user.
    This test simulates a scenario where the API returns a 404 response for the
    "get current user" endpoint. It ensures that the `synthex.users.me()` method
    raises a `NotFoundError` exception when the endpoint is not found.
    Steps:
    1. Mock the API response for the GET request to return a 404 status code with
       an appropriate error message.
    2. Verify that calling `synthex.users.me()` raises the expected `NotFoundError`.
    Args:
        synthex (Synthex): An instance of the Synthex client to test.
    """
    
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/{GET_CURRENT_USER_ENDPOINT}",
        json={
            "status_code": 404,
            "status": "error",
            "message": "Not found",
            "details": None
        },
        status=404
    )

    with pytest.raises(NotFoundError):
        synthex.users.me()