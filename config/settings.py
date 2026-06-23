from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):

    GROQ_API_KEY: str
    GROQ_MODELS: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


