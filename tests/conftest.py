import pytest
import os
from dotenv import load_dotenv

from synthex import Synthex


load_dotenv()


@pytest.fixture(scope="session")
def synthex() -> Synthex:
    """
    Creates and returns an instance of the Synthex class using the API key retrieved from the 
    environment variables.
    Returns:
        Synthex: An instance of the Synthex class initialized with the API key.
    Raises:
        pytest.fail: If the "API_KEY" environment variable is not set.
    """
            
    api_key = os.getenv("API_KEY")
    if not api_key:
        pytest.fail("API_KEY not found in environment variables")
    return Synthex(api_key)