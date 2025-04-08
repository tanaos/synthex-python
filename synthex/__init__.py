from typing import Optional
import os
from dotenv import load_dotenv

from .api_client import APIClient
from .jobs_api import JobsAPI
from .users_api import UsersAPI
from .credits_api import CreditsAPI
from .decorators import handle_validation_errors
from .exceptions import ConfigurationError


@handle_validation_errors
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
    
    def __init__(self, api_key: Optional[str] = None):
        load_dotenv()
        
        if not api_key:
            api_key=os.environ.get("API_KEY")
        if not api_key:
            raise ConfigurationError(
                "An API key is required. Please provide it as an argument or set the API_KEY \
                environment variable."
            )
        self._client = APIClient(api_key)
        self.jobs = JobsAPI(self._client)
        self.users = UsersAPI(self._client)
        self.credits = CreditsAPI(self._client)
        
    def ping(self) -> bool:
        """
        Pings the Synthex API to check if it is reachable.
        Returns:
            bool: True if the API is reachable, False otherwise.
        """
        
        return self._client.ping()