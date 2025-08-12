import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-insecure")
    GDRIVE_JOBDOCS_PENDING_ID=os.getenv("GDRIVE_JOBDOCS_PENDING_ID")
    GDRIVE_JOBDOCS_PROCESSED_ID=os.getenv("GDRIVE_JOBDOCS_PROCESSED_ID")

    @staticmethod
    def validate():
        missing = []
        if not os.getenv("GDRIVE_JOBDOCS_PENDING_ID"): missing.append("GDRIVE_JOBDOCS_PENDING_ID")
        if not os.getenv("GDRIVE_JOBDOCS_PROCESSED_ID"): missing.append("GDRIVE_JOBDOCS_PROCESSED_ID")
        if missing:
            raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
