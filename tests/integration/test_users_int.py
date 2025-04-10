import pytest

from synthex import Synthex
from synthex.models import UserResponseModel


@pytest.mark.integration
def test_me(synthex: Synthex):
    """
    Test the `me` functionality of the Synthex client.
    This test verifies that the `users.me()` method of the Synthex client
    returns an object of type `UserResponseModel`.
    Args:
        synthex (Synthex): An instance of the Synthex client.
    """
    
    user_info = synthex.users.me()
        
    assert isinstance(user_info, UserResponseModel), "User info is not of type UserResponseModel."