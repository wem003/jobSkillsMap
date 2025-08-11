# auth_google.py
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

SCOPES = ["https://www.googleapis.com/auth/drive"]

def main():
    creds = None
    if os.path.exists("../secrets/token.json"):
        creds = Credentials.from_authorized_user_file("../secrets/token.json", SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("../secrets/credentials.json", SCOPES)
        creds = flow.run_local_server(port=0, prompt="consent")
    with open("../secrets/token.json", "w") as token:
        token.write(creds.to_json())
    print("✅ token.json created with scope:", SCOPES)

if __name__ == "__main__":
    main()
