import pytest

from synthex import Synthex


@pytest.mark.integration
def test_ping(synthex: Synthex):
    """
    Test the ping method of the APIClient to ensure it returns True.
    Args:
        synthex (Synthex): An instance of the Synthex class to be tested.
    Asserts:
        The ping method of the api_client returns True.
    """
    
    assert synthex.ping() is True