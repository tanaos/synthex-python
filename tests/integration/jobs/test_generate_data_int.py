import pytest
import os
import csv
from typing import Any

from synthex import Synthex
from synthex.exceptions import ValidationError
  
    
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
        
        
@pytest.mark.integration
def test_generate_data_schema_definition_validation_error(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `schema_definition` is provided.
    This test ensures that a `ValidationError` is raised when the `schema_definition` 
    parameter is set to an incorrect value (e.g., an integer instead of the expected type).
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
    
    try:
        with pytest.raises(ValidationError):
            synthex.jobs.generate_data(
                # Invalid argument type for schema_definition
                schema_definition={
                    "question": {
                        "datatype": "string" #type: ignore
                    },
                    "option-a": {
                        "type": "string"
                    }
                },
                examples=generate_data_params["examples"],
                requirements=generate_data_params["requirements"],
                number_of_samples=generate_data_params["number_of_samples"],
                output_type=generate_data_params["output_type"],
                output_path=generate_data_params["output_path"]
            )
    except AssertionError:
        pytest.fail("Expected ValidationError when an incorrect schema_definition is provided")
        

@pytest.mark.integration
def test_generate_data_examples_validation_error(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `examples` is provided.
    This test ensures that a `ValidationError` is raised when the `examples` 
    parameter is set to an incorrect value (e.g., an integer instead of the expected type).
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
    
    try:
        with pytest.raises(ValidationError):
            synthex.jobs.generate_data(
                schema_definition=generate_data_params["schema_definition"],
                # Invalid argument type for examples
                examples=1, #type: ignore
                requirements=generate_data_params["requirements"],
                number_of_samples=generate_data_params["number_of_samples"],
                output_type=generate_data_params["output_type"],
                output_path=generate_data_params["output_path"]
            )
    except AssertionError:
        pytest.fail("Expected ValidationError when an incorrect examples argument is provided")
        
        
@pytest.mark.integration
def test_generate_data_requirements_validation_error(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `requirements` is provided.
    This test ensures that a `ValidationError` is raised when the `requirements` 
    parameter is set to an incorrect value (e.g., an integer instead of the expected type).
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
    
    try:
        with pytest.raises(ValidationError):
            synthex.jobs.generate_data(
                schema_definition=generate_data_params["schema_definition"],
                examples=generate_data_params["examples"],
                # Invalid argument type for requirements
                requirements=1, #type: ignore
                number_of_samples=generate_data_params["number_of_samples"],
                output_type=generate_data_params["output_type"],
                output_path=generate_data_params["output_path"]
            )
    except AssertionError:
        pytest.fail("Expected ValidationError when an incorrect requirements argument is provided")
        
        
@pytest.mark.integration
def test_generate_data_num_of_samples_validation_error(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `number_of_samples` is provided.
    This test ensures that a `ValidationError` is raised when the `number_of_samples` 
    parameter is set to an incorrect value (e.g., an integer instead of the expected type).
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
    
    try:
        with pytest.raises(ValidationError):
            synthex.jobs.generate_data(
                schema_definition=generate_data_params["schema_definition"],
                examples=generate_data_params["examples"],
                requirements=generate_data_params["requirements"],
                # Invalid argument type for number_of_samples
                number_of_samples=1001,
                output_type=generate_data_params["output_type"],
                output_path=generate_data_params["output_path"]
            )
    except AssertionError:
        pytest.fail("Expected ValidationError when an incorrect number_of_samples argument is provided")
        
        
@pytest.mark.integration
def test_generate_data_output_type_validation_error(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `output_type` is provided.
    This test ensures that a `ValidationError` is raised when the `output_type` 
    parameter is set to an incorrect value (e.g., a string instead of the expected type).
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
    
    try:
        with pytest.raises(ValidationError):
            synthex.jobs.generate_data(
                schema_definition=generate_data_params["schema_definition"],
                examples=generate_data_params["examples"],
                requirements=generate_data_params["requirements"],
                number_of_samples=generate_data_params["number_of_samples"],
                # Invalid argument type for output_type
                output_type="ttt", #type: ignore
                output_path=generate_data_params["output_path"]
            )
    except AssertionError:
        pytest.fail("Expected ValidationError when an incorrect output_type argument is provided")
        
        
@pytest.mark.integration
def test_generate_data_output_path_validation_error(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `output_path` is provided.
    This test ensures that a `ValidationError` is raised when the `output_path` 
    parameter is set to an incorrect value (e.g., an integer instead of the expected type).
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
    
    try:
        with pytest.raises(ValidationError):
            synthex.jobs.generate_data(
                schema_definition=generate_data_params["schema_definition"],
                examples=generate_data_params["examples"],
                requirements=generate_data_params["requirements"],
                number_of_samples=generate_data_params["number_of_samples"],
                output_type=generate_data_params["output_type"],
                # Invalid argument type for output_type
                output_path=1 #type: ignore
            )
    except AssertionError:
        pytest.fail("Expected ValidationError when an incorrect output_path argument is provided")