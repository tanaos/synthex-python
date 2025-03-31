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
        
        
    def _get(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
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


    def _post(self, endpoint: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
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


    def _put(self, endpoint: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
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


    def _delete(self, endpoint: str) -> bool:
        """
        Sends a DELETE request to the specified endpoint and handles the response.
        Args:
            endpoint (str): The API endpoint to send the DELETE request to.
        Returns:
            bool: True if the response status code is 204 (No Content), indicating
                  successful deletion; otherwise, False.
        Raises:
            Any exceptions raised by the `_handle_errors` method if the response
            contains errors.
        """
        
        url = f"{self.BASE_URL}/{endpoint}".rstrip("/")
        response = self.session.delete(url)
        self._handle_errors(response)
        return response.status_code == 204


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
        
        
    def ping(self) -> bool:
        """
        Sends a GET request to the root endpoint (/) to check if the API server is alive.
        Returns True if the server responds with status code 200, False otherwise.
        """
        try:
            self._get("/")
            return True
        except Exception:
            return False