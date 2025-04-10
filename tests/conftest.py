import pytest
import os
from dotenv import load_dotenv
from typing import Any

from synthex import Synthex


load_dotenv()


@pytest.fixture(scope="session")
def synthex() -> Synthex:
    """
    Creates and returns an instance of the Synthex class using the API key 
    from the environment variables.
    Raises:
        pytest.fail: If the "API_KEY" environment variable is not set.
    Returns:
        Synthex: An instance of the Synthex class initialized with the API key.
    """
            
    api_key = os.getenv("API_KEY")
    if not api_key:
        pytest.fail("API_KEY not found in environment variables")
    return Synthex(api_key)


@pytest.fixture(scope="session")
def generate_data_params() -> dict[Any, Any]:
    """
    Fixture to provide parameters for the generate_data method.
    Returns:
        dict: A dictionary containing the required data.
    """
    
    return {
        "schema_definition": {
            "question": {"type": "string"},
            "option-a": {"type": "string"},
            "option-b": {"type": "string"},
            "option-c": {"type": "string"},
            "option-d": {"type": "string"},
            "answer": {"type": "string"}
        },
        "examples": [
            {
                "question": "A gas occupies 6.0 L at 300 K and 1 atm. What is its volume at 600 K and 0.5 atm, assuming ideal gas behavior?",
                "option-a": "12.0 L",
                "option-b": "24.0 L",
                "option-c": "6.0 L",
                "option-d": "3.0 L",
                "answer": "option-b"
            }
        ],
        "requirements": [
            "Question Type: Multiple-choice questions (MCQs)",
            "Difficulty Level: High difficulty, comparable to SAT or AIEEE (JEE Main)",
            "Topic Coverage: Wide range of chemistry topics (physical, organic, inorganic)",
            "Number of Options: Each question must have four answer options",
            "Correct Answer: One of the four options must be correct and clearly marked",
            "Calculation-Based: Include mathematical/calculation-based questions",
            "Indirect Approach: Questions should be indirect and require knowledge application",
            "Conceptual Focus: Emphasize conceptual understanding, problem-solving, and analytical thinking"
        ],
        "number_of_samples": 20,
        "output_type": "csv",
        "output_path": f"test_data/output.csv"
    }