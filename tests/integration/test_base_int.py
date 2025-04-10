import pytest

from synthex import Synthex


@pytest.mark.integration
def test_ping(synthex: Synthex):
    """
    Test the `ping` method of the `Synthex` class.
    This test verifies that the `ping` method returns `True`, indicating
    that the `Synthex` instance is functioning as expected.
    Args:
        synthex (Synthex): An instance of the `Synthex` class to be tested.
    """
    
    assert synthex.ping() is True, "Ping failed, Synthex instance is not functioning as expected."