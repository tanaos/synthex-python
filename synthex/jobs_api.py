from .api_client import APIClient
from typing import Any, List, Literal
import json
import csv
from pydantic import validate_call

from .models import ListJobsResponseModel, SuccessResponse
from .consts import LIST_JOBS_ENDPOINT, CREATE_JOB_WITH_SAMPLES_ENDPOINT


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
            if line and line.startswith("data: "):
                raw = line[6:].strip()
                parsed_data = json.loads(raw)
                with open(output_path, mode="w", newline="", encoding="utf-8") as f:
                    # Write column names
                    writer = csv.DictWriter(f, fieldnames=parsed_data[0].keys())
                    writer.writeheader()
                    # Write each dict as a row
                    writer.writerows(parsed_data)

            
        return SuccessResponse(
            message="Job executed successfully",
        )