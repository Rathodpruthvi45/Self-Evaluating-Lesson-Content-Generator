
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Settings:

    def __init__(self):

        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        self.gemini_model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        if not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Check your .env file."
            )


settings =Settings()