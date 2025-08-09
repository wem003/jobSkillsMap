import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-insecure")
    GDRIVE_PENDING_FOLDER_ID = os.getenv("GDRIVE_PENDING_FOLDER_ID")
    GDRIVE_PROCESSED_FOLDER_ID = os.getenv("GDRIVE_PROCESSED_FOLDER_ID")

    @staticmethod
    def validate():
        missing = []
        if not os.getenv("GDRIVE_PENDING_FOLDER_ID"): missing.append("GDRIVE_PENDING_FOLDER_ID")
        if not os.getenv("GDRIVE_PROCESSED_FOLDER_ID"): missing.append("GDRIVE_PROCESSED_FOLDER_ID")
        if missing:
            raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
