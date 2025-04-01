import pytest

from synthex import Synthex
from synthex.models import UserResponseModel


@pytest.mark.integration
def test_get_current_user(synthex: Synthex):
    """
    Test the `get_current_user` functionality of the Synthex client.
    This test verifies that the `users.me()` method of the Synthex client
    returns an object of type `UserResponseModel`.
    Args:
        synthex (Synthex): An instance of the Synthex client.
    Assertions:
        Asserts that the type of the object returned by `synthex.users.me()`
        is `UserResponseModel`.
    """
    
    
    user_info = synthex.users.me()
    
    print("user info: ", type(user_info))
    
    assert type(user_info) == UserResponseModel