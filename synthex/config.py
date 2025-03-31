from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config(BaseSettings):
    API_BASE_URL: str = "https://compute.tanaos.com"
    
    
config = Config()