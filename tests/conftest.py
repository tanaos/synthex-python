# tests/conftest.py

import pytest
import os
from dotenv import load_dotenv

from synthex.client import APIClient


load_dotenv()

@pytest.fixture(scope="session")
def api_client():
    api_key = os.getenv("API_KEY")
    if not api_key:
        pytest.fail("API_KEY not found in environment variables")
    return APIClient(api_key)
