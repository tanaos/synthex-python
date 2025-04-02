import pytest

from synthex import Synthex
from synthex.models import CreditModel


@pytest.mark.integration
def test_get_current_user(synthex: Synthex):
    """
    Test the `get_current_user` functionality of the `Synthex` instance.
    This test verifies that the `promotional` method of the `credits` attribute
    returns an object of type `CreditModel`.
    Args:
        synthex (Synthex): An instance of the `Synthex` class.
    Asserts:
        The returned value from `synthex.credits.promotional()` is an instance of `CreditModel`.
    """
    
    credits_info = synthex.credits.promotional()
        
    assert isinstance(credits_info, CreditModel)