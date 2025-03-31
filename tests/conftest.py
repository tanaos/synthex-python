# tests/conftest.py

import pytest
import os
from dotenv import load_dotenv

from synthex import Synthex


load_dotenv()

@pytest.fixture(scope="session")
def synthex() -> Synthex:
    api_key = os.getenv("API_KEY")
    if not api_key:
        pytest.fail("API_KEY not found in environment variables")
    return Synthex(api_key)
