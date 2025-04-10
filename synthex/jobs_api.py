from .api_client import APIClient
from typing import Any, List
import json
import csv
from pydantic import validate_call, Field

from .models import ListJobsResponseModel, SuccessResponse, JobOutputDomainType, JobOutputFormats
from .consts import LIST_JOBS_ENDPOINT, CREATE_JOB_WITH_SAMPLES_ENDPOINT
from .decorators import handle_validation_errors
from .exceptions import ValidationError
import os


@handle_validation_errors
class JobsAPI:
    
    def __init__(self, client: APIClient):
        self._client = client
        
    def list(self, limit: int = 10, offset: int = 0) -> ListJobsResponseModel:
        """
        Retrieve a list of jobs with pagination.
        Args:
            limit (int): The maximum number of jobs to retrieve. Defaults to 10.
            offset (int): The number of jobs to skip before starting to retrieve. Defaults to 0.
        Returns:
            ListJobsResponseModel: A model containing the list of jobs and related metadata.
        """
        
        response = self._client.get(f"{LIST_JOBS_ENDPOINT}?limit={limit}&offset={offset}")
        return ListJobsResponseModel.model_validate(response.data)
    
    
    @staticmethod
    def _sanitize_output_path(output_path: str, desired_format: JobOutputFormats) -> str:
        """
        Ensure that the output path is valid, then add the file name to it.
        Args:
            output_path (str): The output path to sanitize.
            format (JobOutputFormats): The desired output format.
        Returns:
            str: The sanitized output path.
        """
        
        # Determine the correct file extension based on the desired format
        correct_extension = f".{desired_format}"
        
        default_file_name = f"synthex-output{correct_extension}"

        # Extract the directory and file name from the output path
        directory, file_name = os.path.split(output_path)
        
        # If a file name is provided, ensure its extension matches the desired format
        if file_name:
            base_name, ext = os.path.splitext(file_name)
            if ext != correct_extension:
                file_name = f"{base_name}{correct_extension}"
        else:
            # If no file name is provided, use a default name with the correct extension
            file_name = default_file_name
        
        # Combine the directory and sanitized file name
        output_path = os.path.join(directory, file_name)
        
        return output_path


    @validate_call
    def generate_data(
        self, 
        schema_definition: JobOutputDomainType,
        examples: List[dict[Any, Any]], 
        requirements: List[str],
        output_path: str,
        number_of_samples: int = Field(..., gt=0, lt=1000), 
        output_type: JobOutputFormats = "csv",
    ) -> SuccessResponse[None]:
        """
        Generates data based on the provided schema definition, examples, and requirements.
        Args:
            schema_definition (dict[Any, Any]): The schema definition that the generated data 
                should conform to.
            examples (List[dict[Any, Any]]): A list of example data points to guide the data 
                generation process.
            requirements (List[str]): A list of specific requirements or constraints for the data 
                generation.
            number_of_samples (int): The number of data samples to generate.
            output_type (Literal["csv"]): The desired output format for the generated data. 
                - "csv": Saves the data to a CSV file.
            output_path (str): The file path where the generated data should be saved.
        Returns:
            SuccessResponse[None]: A response object indicating the success of the job execution.
        Raises:
            ValueError: If the schema_definition or examples are invalid or do not conform to the 
            expected format.
        """
        
        # Sanitize the output path
        output_path = self._sanitize_output_path(output_path, output_type)
        
        # Validate that each example conforms to the schema definition
        for example in examples:
            if set(example.keys()) != set(schema_definition.keys()):
                raise ValidationError("Example keys do not match schema definition keys.")
            
        data: dict[str, Any] = {
            "output_schema": schema_definition,
            "examples": examples,
            "requirements": requirements,
            "datapoint_num": number_of_samples
        }
        
        response = self._client.post_stream(f"{CREATE_JOB_WITH_SAMPLES_ENDPOINT}", data=data)
        
        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        for line in response.iter_lines(decode_unicode=True):
            # Strip "data: " prefix automatically added by the SSE and parse the JSON.
            if line and line.startswith("data: "):
                raw = line[6:].strip()
                parsed_data = json.loads(raw)
                if output_type == "csv":
                    # Write to a .csv file.
                    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
                        # Write column names.
                        writer = csv.DictWriter(f, fieldnames=parsed_data[0].keys())
                        writer.writeheader()
                        # Write each dict as a row.
                        writer.writerows(parsed_data)

            
        return SuccessResponse(
            message="Job executed successfully",
        )