from .api_client import APIClient
from .consts import PING_ENDPOINT


class Synthex:
    def __init__(self, api_key: str):
        self._client = APIClient(api_key)
        
    def ping(self) -> bool:
        """
        Sends a ping request to the server to check connectivity.
        Returns:
            bool: True if the ping request is successful, False otherwise.
        """
        
        try:
            self._client.get(PING_ENDPOINT)
            return True
        except Exception:
            return False