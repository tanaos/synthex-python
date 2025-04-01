from .api_client import APIClient
from .jobs_api import JobsAPI
from .users_api import UsersAPI


class Synthex:
    """
    Synthex is a client library for interacting with the Synthex API.
    Attributes:
        jobs (JobsAPI): Provides access to job-related API operations.
    Methods:
        __init__(api_key: str):
            Initializes the Synthex client with the provided API key.
        ping() -> bool: Pings the Synthex API to check if it is reachable, returns True if 
            reachable, False otherwise.
    """
    
    def __init__(self, api_key: str):
        self._client = APIClient(api_key)
        self.jobs = JobsAPI(self._client)
        self.users = UsersAPI(self._client)
        
    def ping(self) -> bool:
        """
        Pings the Synthex API to check if it is reachable.
        Returns:
            bool: True if the API is reachable, False otherwise.
        """
        
        return self._client.ping()