import pytest
import os
import csv
from typing import Any

from synthex import Synthex
  
    
@pytest.mark.integration
def test_generate_data_success(synthex: Synthex, generate_data_params: dict[Any, Any]):
    """
    Test the `generate_data` method of the `Synthex` class to ensure it generates
    a CSV file with the correct structure and content based on the provided schema,
    examples, and requirements.
    Args:
        synthex (Synthex): An instance of the `Synthex` class used to generate data.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters.
    """
    
    output_path = generate_data_params["output_path"]
    
    synthex.jobs.generate_data(
        schema_definition=generate_data_params["schema_definition"],
        examples=generate_data_params["examples"],
        requirements=generate_data_params["requirements"],
        number_of_samples=generate_data_params["number_of_samples"],
        output_type=generate_data_params["output_type"],
        output_path=output_path
    )
    
    try:
        # Check if the file exists
        assert os.path.exists(output_path), "Output file was not created."

        # Verify the header of the CSV file
        with open(output_path, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            expected_header = ["question", "option-a", "option-b", "option-c", "option-d", "answer"]
            assert header == expected_header, \
                f"CSV header does not match. Expected: {expected_header}, Found: {header}"
    finally:   
        # Clean up the generated file after the test
        os.remove(output_path)