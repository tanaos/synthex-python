import pytest

from synthex import Synthex
from synthex.models import UserResponseModel


@pytest.mark.integration
def test_get_current_user(synthex: Synthex):
    """
    Test the me method of the UsersAPI to ensure it retrieves user information.
    Args:
        synthex (Synthex): An instance of the Synthex class to be tested.
    Asserts:
        The get_current_user method of the UsersAPI returns a UserResponseModel object.
    """
    
    user_info = synthex.users.me()
    
    print("user info: ", type(user_info))
    
    assert type(user_info) == UserResponseModel