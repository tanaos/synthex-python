from .api_client import APIClient

from .endpoints import GET_PROMOTIONAL_CREDITS_ENDPOINT
from .models import CreditModel


class CreditsAPI:
    
    def __init__(self, client: APIClient):
        self._client = client
        
        
    def promotional(self) -> CreditModel:
        """
        Retrieve promotional credits information.
        Returns:
            CreditModel: An instance of `CreditModel` containing the promotional credits data.
        """
        
        response = self._client.get(GET_PROMOTIONAL_CREDITS_ENDPOINT)
        return CreditModel.model_validate(response.data)