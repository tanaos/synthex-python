from .api_client import APIClient
from typing import Any, List, Literal
import json
import csv
from pydantic import validate_call, Field

from .models import ListJobsResponseModel, SuccessResponse, JobOutputDomainType
from .consts import LIST_JOBS_ENDPOINT, CREATE_JOB_WITH_SAMPLES_ENDPOINT
from .decorators import handle_validation_errors
from .exceptions import ValidationError


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
        self, 
        schema_definition: JobOutputDomainType,
        examples: List[dict[Any, Any]], 
        requirements: List[str],
        output_path: str,
        number_of_samples: int = Field(..., gt=0, lt=1000), 
        output_type: Literal["csv"] = "csv",
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