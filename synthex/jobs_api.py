from .api_client import APIClient
from typing import Any, List, Literal
import json
import csv
from pydantic import validate_call

from .models import ListJobsResponseModel, SuccessResponse
from .consts import LIST_JOBS_ENDPOINT, CREATE_JOB_WITH_SAMPLES_ENDPOINT
from .decorators import handle_validation_errors


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
    
    @validate_call
    def generate_data(
        self, schema_definition: dict[Any, Any], examples: List[dict[Any, Any]], 
        requirements: List[str], number_of_samples: int, output_type: Literal["csv", "pandas"], 
        output_path: str
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
            output_type (Literal["csv", "pandas"]): The desired output format for the generated data. 
                - "csv": Saves the data to a CSV file.
                - "pandas": Returns the data as a pandas DataFrame.
            output_path (str): The file path where the generated data should be saved.
        Returns:
            SuccessResponse[None]: A response object indicating the success of the job execution.
        Raises:
            ValueError: If the schema_definition or examples are invalid or do not conform to the expected format.
            JSONDecodeError: If the response data cannot be parsed as valid JSON.
            IOError: If there is an issue writing the CSV file to the specified output path.
        """
        
        # TODO: validate schema_definition and examples: they need to be valid JSONs and conform
        # to the output schema definition type.
        
        data: dict[str, Any] = {
            "output_schema": schema_definition,
            "examples": examples,
            "requirements": requirements,
            "datapoint_num": number_of_samples
        }
        
        response = self._client.post_stream(f"{CREATE_JOB_WITH_SAMPLES_ENDPOINT}", data=data)
        
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