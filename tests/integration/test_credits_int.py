import pytest

from synthex import Synthex
from synthex.models import CreditModel


@pytest.mark.integration
def test_promotional(synthex: Synthex):
    """
    Test the `promotional` functionality of the `Synthex` instance.
    This test verifies that the `promotional` method of the `credits` attribute
    returns an object of type `CreditModel`.
    Args:
        synthex (Synthex): An instance of the `Synthex` class.
    """
    
    credits_info = synthex.credits.promotional()
        
    assert isinstance(credits_info, CreditModel), "Promotional credits info is not of type CreditModel."