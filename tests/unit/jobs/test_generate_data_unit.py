import responses
from typing import Any
import os
import csv

from synthex import Synthex
from synthex.endpoints import API_BASE_URL, CREATE_JOB_WITH_SAMPLES_ENDPOINT
from synthex.config import OUTPUT_FILE_DEFAULT_NAME


json_body="data: [{\"question\": \"What is the enthalpy change for the combustion of 1 mole of methane?\",\
    \"option-a\": \"-890 kJ/mol\", \"option-b\": \"-500 kJ/mol\", \"option-c\": \"-1000 kJ/mol\", \"option-d\":\
    \"-750 kJ/mol\", \"answer\": \"option-a\"}]\n\n"


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
        
        
@responses.activate
def test_generate_data_output_type_extension_mismatch(synthex: Synthex, generate_data_params: dict[Any, Any]):
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


@responses.activate
def test_generate_data_output_path_extensionless_file(synthex: Synthex, generate_data_params: dict[Any, Any]):
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


@responses.activate
def test_generate_data_output_path_no_filename(synthex: Synthex, generate_data_params: dict[Any, Any]):
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
