from synthex.client import APIClient


class SynthexAPI:
    def __init__(self, client: APIClient):
        self.client = client