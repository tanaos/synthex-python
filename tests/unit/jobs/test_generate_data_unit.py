import responses
from typing import Any
import os
import csv
import pytest

from synthex import Synthex
from synthex.endpoints import API_BASE_URL, CREATE_JOB_WITH_SAMPLES_ENDPOINT
from synthex.config import OUTPUT_FILE_DEFAULT_NAME
from synthex.exceptions import ValidationError


json_body="data: [{\"question\": \"What is the enthalpy change for the combustion of 1 mole of methane?\",\
    \"option-a\": \"-890 kJ/mol\", \"option-b\": \"-500 kJ/mol\", \"option-c\": \"-1000 kJ/mol\", \"option-d\":\
    \"-750 kJ/mol\", \"answer\": \"option-a\"}]\n\n"


@pytest.mark.unit
@responses.activate
def test_generate_data_success(synthex: Synthex, generate_data_params: dict[Any, Any]):
    """
    Test the successful generation of data using the `generate_data` method of the `Synthex` class.
    This test mocks an SSE (Server-Sent Events) response for a POST request to the 
    `CREATE_JOB_WITH_SAMPLES_ENDPOINT` and verifies that the `generate_data` method:
    1. Creates the expected output file.
    2. Writes the correct header to the output CSV file.
    Args:
        synthex (Synthex): An instance of the `Synthex` class.
        generate_data_params (dict[Any, Any]): A dictionary containing parameters for the `generate_data` method
    """
      
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/{CREATE_JOB_WITH_SAMPLES_ENDPOINT}",
        # Mock SSE data.
        body=json_body,
        content_type="text/event-stream",
        status=200
    )
    
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


@pytest.mark.unit
@responses.activate
def test_generate_data_output_type_extension_mismatch(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test to ensure that, if the `output_path` and `output_type` parameters of the `generate_data` 
    method of the `Synthex` class are not consistent (e.g. output_type="csv" but output_path ends 
    in ".pdf"), the function replaces the incorrect extension with the correct one.
    Args:
        synthex (Synthex): An instance of the `Synthex` class.
        generate_data_params (dict[Any, Any]): A dictionary containing parameters
            required for the `generate_data` method.
    """
    
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/{CREATE_JOB_WITH_SAMPLES_ENDPOINT}",
        # Mock SSE data.
        body=json_body,
        content_type="text/event-stream",
        status=200
    )
    
    incorrect_output_path = "test_data/output.pdf"
    correct_output_path = f"test_data/output.{generate_data_params["output_type"]}"
        
    synthex.jobs.generate_data(
        schema_definition=generate_data_params["schema_definition"],
        examples=generate_data_params["examples"],
        requirements=generate_data_params["requirements"],
        number_of_samples=generate_data_params["number_of_samples"],
        output_type=generate_data_params["output_type"],
        output_path=incorrect_output_path
    )
    
    try:
        # Ensure that the file with the wrong extension was not created
        assert not os.path.exists(incorrect_output_path), "Output file was created with the wrong extension."
        # Check whether the file with the correct extension was created
        assert os.path.exists(correct_output_path), "Output file with the correct extension was not created."

        # Verify the header of the CSV file
        with open(correct_output_path, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            expected_header = ["question", "option-a", "option-b", "option-c", "option-d", "answer"]
            assert header == expected_header, \
                f"CSV header does not match. Expected: {expected_header}, Found: {header}"
    finally:   
        # Clean up the generated file after the test
        os.remove(correct_output_path)


@pytest.mark.unit
@responses.activate
def test_generate_data_output_path_extensionless_file(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test to ensure that, if the `output_path` parameter of the `generate_data` method of the `Synthex` class 
    specifies a file with no extension (e.g. "/output/test"), the function adds an extension that is consistent
    with the `output_type` parameter.
    Args:
        synthex (Synthex): An instance of the `Synthex` class.
        generate_data_params (dict[Any, Any]): A dictionary containing parameters
            required for the `generate_data` method.
    """
    
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/{CREATE_JOB_WITH_SAMPLES_ENDPOINT}",
        # Mock SSE data.
        body=json_body,
        content_type="text/event-stream",
        status=200
    )
    
    extensionless_output_path = "test_data/output"
    correct_output_path = f"test_data/output.{generate_data_params["output_type"]}"
        
    synthex.jobs.generate_data(
        schema_definition=generate_data_params["schema_definition"],
        examples=generate_data_params["examples"],
        requirements=generate_data_params["requirements"],
        number_of_samples=generate_data_params["number_of_samples"],
        output_type=generate_data_params["output_type"],
        output_path=extensionless_output_path
    )
    
    try:
        # Ensure that the extensionless file was not created
        assert not os.path.exists(extensionless_output_path), "Output file with no extension was created."
        # Check whether the file with the correct extension was created
        assert os.path.exists(correct_output_path), "Output file with the correct extension was not created."

        # Verify the header of the CSV file
        with open(correct_output_path, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            expected_header = ["question", "option-a", "option-b", "option-c", "option-d", "answer"]
            assert header == expected_header, \
                f"CSV header does not match. Expected: {expected_header}, Found: {header}"
    finally:   
        # Clean up the generated file after the test
        os.remove(correct_output_path)


@pytest.mark.unit
@responses.activate
def test_generate_data_output_path_no_filename(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test to ensure that, if the `output_path` parameter of the `generate_data` method of the `Synthex` class 
    specifies a path but not a file name, the function attaches the default file name with an extension that is
    consistent with the `output_type` parameter.
    Args:
        synthex (Synthex): An instance of the `Synthex` class.
        generate_data_params (dict[Any, Any]): A dictionary containing parameters
            required for the `generate_data` method.
    """
    
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/{CREATE_JOB_WITH_SAMPLES_ENDPOINT}",
        # Mock SSE data.
        body=json_body,
        content_type="text/event-stream",
        status=200
    )
    
    output_path_with_no_filename = "test_data/"
    correct_output_path = f"test_data/{OUTPUT_FILE_DEFAULT_NAME(generate_data_params["output_type"])}"
        
    synthex.jobs.generate_data(
        schema_definition=generate_data_params["schema_definition"],
        examples=generate_data_params["examples"],
        requirements=generate_data_params["requirements"],
        number_of_samples=generate_data_params["number_of_samples"],
        output_type=generate_data_params["output_type"],
        output_path=output_path_with_no_filename
    )
    
    try:
        # Check whether the file with the default name and correct extension was created
        assert os.path.exists(correct_output_path), "Output file with the correct extension was not created."

        # Verify the header of the CSV file
        with open(correct_output_path, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            expected_header = ["question", "option-a", "option-b", "option-c", "option-d", "answer"]
            assert header == expected_header, \
                f"CSV header does not match. Expected: {expected_header}, Found: {header}"
    finally:   
        # Clean up the generated file after the test
        os.remove(correct_output_path)
        

@pytest.mark.unit
def test_generate_data_schema_definition_wrong_type(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `schema_definition` is provided. This test ensures that a `ValidationError` is raised when 
    the `schema_definition` parameter has an incorrect type (e.g., an integer instead of 
    the expected type).
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` 
            method.
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


@pytest.mark.unit
def test_generate_data_examples_wrong_type(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `examples` is provided. This test ensures that a `ValidationError` is raised when the 
    `examples` parameter has an incorrect type (e.g., an integer instead of the 
    expected type).
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` 
            method.
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


@pytest.mark.unit
def test_generate_data_examples_schema_definition_mismatch(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `examples` is provided. This test ensures that a `ValidationError` is raised when the 
    `examples` parameter is inconsistent with the `schema_definition` parameter (e.g.,
    the `examples` parameter contains fields that are not present in the `schema_definition`).
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` 
            method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
    
    try:
        with pytest.raises(ValidationError):
            synthex.jobs.generate_data(
                schema_definition=generate_data_params["schema_definition"],
                # Invalid argument type for examples
                examples=[{
                    "question": "Random question",
                    "option-a": "12.0 L",
                    "option-b": "24.0 L",
                    "option-c": "6.0 L",
                    "option-d": "3.0 L",
                    # "Answer" field is missing
                }],
                requirements=generate_data_params["requirements"],
                number_of_samples=generate_data_params["number_of_samples"],
                output_type=generate_data_params["output_type"],
                output_path=generate_data_params["output_path"]
            )
    except AssertionError:
        pytest.fail(
            "Expected ValidationError when the examples argument is inconsistent with \
            the schema_definition argument"
        )


@pytest.mark.unit
def test_generate_data_requirements_wrong_type(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `requirements` is provided. This test ensures that a `ValidationError` is raised when 
    the `requirements` parameter has an incorrect type (e.g., a string instead of the 
    expected list of strings).
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` 
            method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
    
    try:
        with pytest.raises(ValidationError):
            synthex.jobs.generate_data(
                schema_definition=generate_data_params["schema_definition"],
                examples=generate_data_params["examples"],
                # Invalid argument type for requirements
                requirements="Sample requirement", #type: ignore
                number_of_samples=generate_data_params["number_of_samples"],
                output_type=generate_data_params["output_type"],
                output_path=generate_data_params["output_path"]
            )
    except AssertionError:
        pytest.fail("Expected ValidationError when an incorrect requirements argument is provided")
        

@pytest.mark.unit
def test_generate_data_num_of_samples_wrong_type(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `number_of_samples` is provided. This test ensures that a `ValidationError` is raised when 
    the `number_of_samples` parameter has an incorrect type (e.g., a string instead of 
    the expected integer).
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
                number_of_samples="test", #type: ignore
                output_type=generate_data_params["output_type"],
                output_path=generate_data_params["output_path"]
            )
    except AssertionError:
        pytest.fail("Expected ValidationError when an incorrect number_of_samples argument \
            is provided")
        

@pytest.mark.unit
def test_generate_data_num_of_samples_value_too_high(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `number_of_samples` is provided. This test ensures that a `ValidationError` is raised when 
    the `number_of_samples` parameter has a value that is larger than the maximum allowed value.
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
                # Invalid argument type for number_of_samples: maximum allowed value is 1000
                number_of_samples=1001,
                output_type=generate_data_params["output_type"],
                output_path=generate_data_params["output_path"]
            )
    except AssertionError:
        pytest.fail("Expected ValidationError when an incorrect number_of_samples argument \
            is provided")
        
        
@pytest.mark.unit
def test_generate_data_output_type_wrong_type(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `output_type` is provided. This test ensures that a `ValidationError` is raised when the 
    `output_type` parameter has an incorrect type (e.g., an unallowed string).
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
        

@pytest.mark.unit
def test_generate_data_output_path_wrong_type(
    synthex: Synthex, generate_data_params: dict[Any, Any]
):
    """
    Test case for validating the behavior of the `generate_data` method when an invalid 
    `output_path` is provided. This test ensures that a `ValidationError` is raised when 
    the `output_path` parameter has an incorrect type (e.g., an integer instead of 
    the expected type).
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` 
            method.
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
