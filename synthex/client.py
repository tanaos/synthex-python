import requests
from typing import Optional, Any

from synthex.config import config


class APIClient:
    BASE_URL = config.API_BASE_URL
    
    def __init__(self, api_key: str):
        self.API_KEY = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.API_KEY}",
            "Accept": "application/json",
        })
        
        
    def get(self, endpoint: str, params: Optional[dict[str, Any]] = None):
        """
        Sends a GET request to the specified endpoint with optional query parameters.
        Args:
            endpoint (str): The API endpoint to send the GET request to.
            params (Optional[dict[str, Any]]): A dictionary of query parameters to include in the 
                request. Defaults to None.
        Returns:
            dict: The JSON response from the server.
        Raises:
            HTTPError: If the response contains an HTTP error status code.
        """
        
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params)
        self._handle_errors(response)
        return response.json()
    
    
    def _handle_errors(self, response: requests.Response) -> None:
        """
        Handles HTTP response errors by checking the response status.
        Args:
            response (requests.Response): The HTTP response object to evaluate.
        Raises:
            Exception: If the response status is not OK (e.g., status code is not 2xx),
                an exception is raised with the status code and response text.
        """
        
        if not response.ok:
            raise Exception(f"Error {response.status_code}: {response.text}")
        
        
    def ping(self) -> bool:
        """
        Sends a GET request to the root endpoint (/) to check if the API server is alive.
        Returns True if the server responds with status code 200. Raises an exception otherwise.
        """
        url = f"{self.BASE_URL}/"
        response = self.session.get(url)
        self._handle_errors(response)
        return response.status_code == 200