import requests
from typing import Optional, Any

from .endpoints import API_BASE_URL, PING_ENDPOINT
from .models import SuccessResponse
from .exceptions import *


class APIClient:
    """
    A utility class for interacting with a RESTful API. It provides methods for sending HTTP 
    requests to specified endpoints, handling errors, and managing authentication headers.
    Attributes:
        BASE_URL (str): The base URL of the API.
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
    
    BASE_URL = API_BASE_URL
    
    def __init__(self, api_key: str):
        self.API_KEY = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": f"{self.API_KEY}",
            "Accept": "application/json",
        })
        
        
    def _handle_errors(self, response: requests.Response) -> None:
        """
        Handles HTTP response errors by raising appropriate exceptions based on the status code.
        Args:
            response (requests.Response): The HTTP response object to evaluate.
        Raises:
            AuthenticationError: If the response status code is 401 (Unauthorized).
            NotFoundError: If the response status code is 404 (Not Found).
            RateLimitError: If the response status code is 429 (Rate Limit Exceeded).
            ServerError: If the response status code is in the range 500-599 (Server Error).
        """
                
        try:
            error_details = response.json()
        except ValueError:
            error_details = response.text
        
        status = response.status_code
                        
        if status == 401:
            raise AuthenticationError("Unauthorized", status, response.url, error_details)
        elif status == 404:
            raise NotFoundError("Not found", status, response.url, error_details)
        elif status == 429:
            raise RateLimitError("Rate limit exceeded", status, response.url, error_details)
        elif 500 <= status < 600:
            raise ServerError("Server error", status, response.url, error_details)
                
        
    def get(
        self, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> SuccessResponse[Any]:
        """
        Sends a GET request to the specified API endpoint.
        Args:
            endpoint (str): The API endpoint to send the GET request to.
            params (Optional[dict[str, Any]]): Optional query parameters to include in the request.
        Returns:
            SuccessResponse[Any]: A response object containing the parsed JSON data.
        Raises:
            SynthexError: If the response contains an HTTP error status code.
        """
        
        url = f"{self.BASE_URL}/{endpoint}".rstrip("/")
        response = self.session.get(url, params=params)
        self._handle_errors(response)
        return SuccessResponse(**response.json())


    def post(
        self, endpoint: str, data: Optional[dict[str, Any]] = None
    ) -> SuccessResponse[Any]:
        """
        Sends a POST request to the specified endpoint with the provided data.
        Args:
            endpoint (str): The API endpoint to send the POST request to.
            data (Optional[dict[str, Any]]): The JSON-serializable data to include in the request body. Defaults to None.
        Returns:
            SuccessResponse[Any]: The JSON response from the server.
        Raises:
            SynthexError: If the response contains an HTTP error status code.
        """
        
        url = f"{self.BASE_URL}/{endpoint}".rstrip("/")
        response = self.session.post(url, json=data)
        self._handle_errors(response)
        return SuccessResponse(**response.json())


    def put(
        self, endpoint: str, data: Optional[dict[str, Any]] = None
    ) -> SuccessResponse[Any]:
        """
        Sends a PUT request to the specified endpoint with the provided data.
        Args:
            endpoint (str): The API endpoint to send the PUT request to.
            data (Optional[dict[str, Any]]): The JSON-serializable dictionary to include in the request body. Defaults to None.
        Returns:
            SuccessResponse[Any]: The JSON response from the server.
        Raises:
            SynthexError: If the response contains an HTTP error status code.
        """
        
        url = f"{self.BASE_URL}/{endpoint}".rstrip("/")
        response = self.session.put(url, json=data)
        self._handle_errors(response)
        return SuccessResponse(**response.json())


    def delete(self, endpoint: str) -> SuccessResponse[Any]:
        """
        Sends a DELETE request to the specified endpoint and handles the response.
        Args:
            endpoint (str): The API endpoint to send the DELETE request to.
        Returns:
            SuccessResponse[Any]: The JSON response from the server.
        Raises:
            SynthexError: If the response contains an HTTP error status code.
        """
        
        url = f"{self.BASE_URL}/{endpoint}".rstrip("/")
        response = self.session.delete(url)
        self._handle_errors(response)
        return SuccessResponse(**response.json())
    
    
    def post_stream(
        self, endpoint: str, data: Optional[dict[str, Any]] = None
    ) -> requests.Response:
        """
        Sends a POST request to the specified API endpoint and streams the response.
        Args:
            endpoint (str): The API endpoint to send the POST request to.
            data (Optional[dict[str, Any]]): The JSON-serializable data to include in the request body. Defaults to None.
        Returns:
            requests.Response: The raw HTTP response object for streaming.
        Raises:
            SynthexError: If the response contains an HTTP error status code.
        """
        
        url = f"{self.BASE_URL}/{endpoint}".rstrip("/")
        response = self.session.post(url, json=data, stream=True)
        self._handle_errors(response)
        return response
    
    
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