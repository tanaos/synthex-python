import responses
from typing import Any
import os
import csv

from synthex import Synthex
from synthex.consts import API_BASE_URL, CREATE_JOB_WITH_SAMPLES_ENDPOINT


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
        body="data: [{\"question\": \"What is the enthalpy change for the combustion of 1 mole of methane?\",\
        \"option-a\": \"-890 kJ/mol\", \"option-b\": \"-500 kJ/mol\", \"option-c\": \"-1000 kJ/mol\", \"option-d\":\
        \"-750 kJ/mol\", \"answer\": \"option-a\"}]\n\n",
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
        with open("./test_data/output.csv", mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            expected_header = ["question", "option-a", "option-b", "option-c", "option-d", "answer"]
            assert header == expected_header, \
                f"CSV header does not match. Expected: {expected_header}, Found: {header}"
    finally:   
        # Clean up the generated file after the test
        os.remove(output_path)