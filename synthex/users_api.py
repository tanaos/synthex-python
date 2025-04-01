from .api_client import APIClient

from .consts import GET_CURRENT_USER_ENDPOINT
from .models import UserResponseModel


class UsersAPI:
    def __init__(self, client: APIClient):
        self._client = client
        
    def get_current_user(self) -> UserResponseModel:
        """
        Retrieves the current user's information from the API.

        Returns:
            UserResponseModel: A model containing the current user's information.
        """
        
        data = self._client.get(GET_CURRENT_USER_ENDPOINT)
        return UserResponseModel(**data)