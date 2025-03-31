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
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params)
        self._handle_errors(response)
        return response.json()
    
    
    def _handle_errors(self, response: requests.Response) -> None:
        if not response.ok:
            raise Exception(f"Error {response.status_code}: {response.text}")