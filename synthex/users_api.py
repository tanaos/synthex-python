from .api_client import APIClient

from .endpoints import GET_CURRENT_USER_ENDPOINT
from .models import UserResponseModel


class UsersAPI:
    
    def __init__(self, client: APIClient):
        self._client = client
        
        
    def me(self) -> UserResponseModel:
        """
        Retrieves the current user's information from the API.

        Returns:
            UserResponseModel: A model containing the current user's information.
        """
        
        response = self._client.get(GET_CURRENT_USER_ENDPOINT)
        return UserResponseModel.model_validate(response.data)