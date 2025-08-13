import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GDRIVE_JOBDOCS_PENDING_ID=os.getenv("GDRIVE_JOBDOCS_PENDING_ID")
    GDRIVE_JOBDOCS_PROCESSED_ID=os.getenv("GDRIVE_JOBDOCS_PROCESSED_ID")
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

    @staticmethod
    def validate():
        missing = []
        if not os.getenv("GDRIVE_JOBDOCS_PENDING_ID"): missing.append("GDRIVE_JOBDOCS_PENDING_ID")
        if not os.getenv("GDRIVE_JOBDOCS_PROCESSED_ID"): missing.append("GDRIVE_JOBDOCS_PROCESSED_ID")
        if not os.getenv("GOOGLE_SHEET_ID"): missing.append("GOOGLE_SHEET_ID")
        if missing:
            raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
