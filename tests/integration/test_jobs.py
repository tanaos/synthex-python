import pytest

from synthex import Synthex
from synthex.models import ListJobsResponseModel


@pytest.mark.integration
def test_list_jobs(synthex: Synthex):
    """
    Test the `list` method of the `jobs` attribute in the `Synthex` class.
    This test verifies that the `list` method of `synthex.jobs` returns an 
    instance of `ListJobsResponseModel`.
    Args:
        synthex (Synthex): An instance of the `Synthex` class.
    Asserts:
        The returned value from `synthex.jobs.list()` is an instance of 
        `ListJobsResponseModel`.
    """
    
    jobs_info = synthex.jobs.list()
    print("jobs_info: ", jobs_info)
        
    assert isinstance(jobs_info, ListJobsResponseModel)
    
    
@pytest.mark.integration
def test_generate_data(synthex: Synthex):
    """
    Test the `generate_data` method of the `jobs` attribute in the `Synthex` class.
    This test verifies that the `generate_data` method of `synthex.jobs` does not raise 
    any exceptions when called with valid parameters.
    Args:
        synthex (Synthex): An instance of the `Synthex` class.
    Asserts:
        The `generate_data` method does not raise any exceptions.
    """
    
    schema_definition = {
        "question": {"type": "string"},
        "option-a": {"type": "string"},
        "option-b": {"type": "string"},
        "option-c": {"type": "string"},
        "option-d": {"type": "string"},
        "answer": {"type": "string"}
    }
    
    examples = [
        {
            "question": "A gas occupies 6.0 L at 300 K and 1 atm. What is its volume at 600 K and 0.5 atm, assuming ideal gas behavior?",
            "option-a": "12.0 L",
            "option-b": "24.0 L",
            "option-c": "6.0 L",
            "option-d": "3.0 L",
            "answer": "option-b"
        }
    ]
    
    requirements = [
        "Question Type: Multiple-choice questions (MCQs)",
        "Difficulty Level: High difficulty, comparable to SAT or AIEEE (JEE Main)",
        "Topic Coverage: Wide range of chemistry topics (physical, organic, inorganic)",
        "Number of Options: Each question must have four answer options",
        "Correct Answer: One of the four options must be correct and clearly marked",
        "Calculation-Based: Include mathematical/calculation-based questions",
        "Indirect Approach: Questions should be indirect and require knowledge application",
        "Conceptual Focus: Emphasize conceptual understanding, problem-solving, and analytical thinking"
    ]
    
    number_of_samples = 10
    
    response = synthex.jobs.generate_data(
        schema_definition=schema_definition,
        examples=examples,
        requirements=requirements,
        number_of_samples=number_of_samples
    )
    
    print(response)