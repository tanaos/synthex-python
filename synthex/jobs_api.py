from .api_client import APIClient


class JobsAPI:
    def __init__(self, client: APIClient):
        self._client = client