from .client import APIClient
from .endpoint import SynthexAPI


class Synthex:
    def __init__(self, api_key: str):
        self.client = APIClient(api_key)
        self.synthex = SynthexAPI(self.client)