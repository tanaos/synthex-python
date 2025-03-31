import requests
from typing import Optional, Any

from .config import config
from .consts import PING_ENDPOINT


class APIClient:
    """
    A utility class for interacting with a RESTful API. It provides methods for sending HTTP 
    requests to specified endpoints, handling errors, and managing authentication headers.
    Attributes:
        BASE_URL (str): The base URL of the API, retrieved from the configuration.
        API_KEY (str): The API key used for authentication.
        session (requests.Session): A persistent session object for making HTTP requests.
    Methods:
        __init__(api_key: str): 
            Initializes the APIClient with the provided API key and sets up the session headers.
        _handle_errors(response: requests.Response) -> None:
            Handles HTTP errors in the API response. Raises an HTTPError for non-2xx status codes.
        get(endpoint: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
            Sends a GET request to the specified endpoint with optional query parameters and 
            returns the JSON response.
        post(endpoint: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
            Sends a POST request to the specified endpoint with the provided data and returns the 
            JSON response.
        put(endpoint: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
            Sends a PUT request to the specified endpoint with the provided data and returns the 
            JSON response.
        delete(endpoint: str) -> bool: 
            Sends a DELETE request to the specified endpoint and returns True if successful.
        ping() -> bool: 
            Sends a ping request to the server to check connectivity. Returns True if successful,
            False otherwise.
    """
    
    BASE_URL = config.API_BASE_URL
    
    def __init__(self, api_key: str):
        self.API_KEY = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.API_KEY}",
            "Accept": "application/json",
        })
        
        
    def _handle_errors(self, response: requests.Response) -> None:
        """
        Handles HTTP errors in the API response.
        Args:
            response (requests.Response): The HTTP response object to check for errors.
        Raises:
            requests.HTTPError: If the response status indicates a failure (non-2xx status code),
                an HTTPError is raised with the status code and response text.
        """
        
        if not response.ok:
            raise requests.HTTPError(
                f"API Error {response.status_code}: {response.text}",
                response=response
            )
        
        
    def get(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """
        Sends a GET request to the specified endpoint with optional query parameters.
        Args:
            endpoint (str): The API endpoint to send the GET request to.
            params (Optional[dict[str, Any]]): A dictionary of query parameters to include in the request. Defaults to None.
        Returns:
            dict[str, Any]: The JSON response from the server as a dictionary.
        Raises:
            HTTPError: If the response contains an HTTP error status code.
        """
        
        url = f"{self.BASE_URL}/{endpoint}".rstrip("/")
        response = self.session.get(url, params=params)
        self._handle_errors(response)
        return response.json()


    def post(self, endpoint: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """
        Sends a POST request to the specified endpoint with the provided data.
        Args:
            endpoint (str): The API endpoint to send the POST request to.
            data (Optional[dict[str, Any]]): The JSON-serializable data to include in the request body. Defaults to None.
        Returns:
            dict[str, Any]: The JSON response from the server.
        Raises:
            HTTPError: If the response contains an HTTP error status code.
        """
        
        url = f"{self.BASE_URL}/{endpoint}".rstrip("/")
        response = self.session.post(url, json=data)
        self._handle_errors(response)
        return response.json()


    def put(self, endpoint: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """
        Sends a PUT request to the specified endpoint with the provided data.
        Args:
            endpoint (str): The API endpoint to send the PUT request to.
            data (Optional[dict[str, Any]]): The JSON-serializable dictionary to include in the request body. Defaults to None.
        Returns:
            dict[str, Any]: The JSON response from the server.
        Raises:
            HTTPError: If the response contains an HTTP error status code.
        """
        
        url = f"{self.BASE_URL}/{endpoint}".rstrip("/")
        response = self.session.put(url, json=data)
        self._handle_errors(response)
        return response.json()


    def delete(self, endpoint: str) -> bool:
        """
        Sends a DELETE request to the specified endpoint and handles the response.
        Args:
            endpoint (str): The API endpoint to send the DELETE request to.
        Returns:
            bool: True if the response status code is 204 (No Content), indicating
                  successful deletion; otherwise, False.
        Raises:
            HTTPError: If the response contains an HTTP error status code.
        """
        
        url = f"{self.BASE_URL}/{endpoint}".rstrip("/")
        response = self.session.delete(url)
        self._handle_errors(response)
        return response.status_code == 200
    
    
    def ping(self) -> bool:
        """
        Sends a ping request to the server to check connectivity.
        Returns:
            bool: True if the ping request is successful, False otherwise.
        """
        
        try:
            self.get(PING_ENDPOINT)
            return True
        except Exception:
            return False