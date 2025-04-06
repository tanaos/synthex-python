from .api_client import APIClient

from .models import ListJobsResponseModel
from .consts import LIST_JOBS_ENDPOINT, API_JOB_ENDPOINT


class JobsAPI:
    
    def __init__(self, client: APIClient):
        self._client = client
        
    def list_x(self, limit: int = 10, offset: int = 0) -> ListJobsResponseModel:
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
    
    
    def generate_data(
        self, schema_definition: dict, examples: list[dict], requirements: list[str],
        number_of_samples: int, output_type: str = "json"
    ) -> None:
        
        # TODO: validate schema_definition and examples: they need to be valid JSONs and conform
        # to the output schema definition type.
        
        data = {
            "output_schema": schema_definition,
            "examples": examples,
            "requirements": requirements,
            "datapoint_num": number_of_samples
        }
        
        response = self._client.post(f"{API_JOB_ENDPOINT}", data=data)