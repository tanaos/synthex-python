import pytest
import os
import csv

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
        
    assert isinstance(jobs_info, ListJobsResponseModel), \
        f"Expected ListJobsResponseModel, but got {type(jobs_info)}"
    
    
@pytest.mark.integration
def test_generate_data(synthex: Synthex):
    """
    Test the `generate_data` method of the `Synthex` class to ensure it generates
    a CSV file with the correct structure and content based on the provided schema,
    examples, and requirements.
    This test performs the following checks:
    1. Verifies that the output file is created at the specified path.
    2. Ensures the header of the generated CSV file matches the expected schema.
    Args:
        synthex (Synthex): An instance of the `Synthex` class used to generate data.
    Output:
        - A CSV file is generated at the specified output path with the required
          structure and content.
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
    number_of_samples = 20
    
    output_path = f"./test_data/output.csv"
    
    synthex.jobs.generate_data(
        schema_definition=schema_definition,
        examples=examples,
        requirements=requirements,
        number_of_samples=number_of_samples,
        output_type="csv",
        output_path=output_path,
    )
    
    try:
        # Check if the file exists
        assert os.path.exists(output_path), "Output file was not created."

        # Verify the header of the CSV file
        with open("./test_data/output.csv", mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            expected_header = ["question", "option-a", "option-b", "option-c", "option-d", "answer"]
            assert header == expected_header, \
                f"CSV header does not match. Expected: {expected_header}, Found: {header}"
    finally:   
        # Clean up the generated file after the test
        os.remove(output_path)