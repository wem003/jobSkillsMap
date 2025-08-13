from __future__ import annotations
import io, os, re, json
from dataclasses import dataclass
from datetime import datetime
from typing import List

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# NEW imports for robust token handling
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

# ---- OAuth settings ----
SCOPES = ["https://www.googleapis.com/auth/drive"]
SECRETS_DIR = os.getenv("SECRETS_DIR", os.getenv("SECRETS_DIR".lower(), "secrets"))
CREDS_PATH = os.path.join(SECRETS_DIR, "credentials.json")
TOKEN_PATH = os.path.join(SECRETS_DIR, "token.json")


# ---- OAuth settings ----
#SCOPES = ["https://www.googleapis.com/auth/drive"]
#TOKEN_PATH = "token.json"          # persisted after first auth
#CREDS_PATH = "credentials.json"    # downloaded from Google Cloud console

@dataclass
class DriveFile:
    id: str
    name: str
    size_kb: int
    mtime: str  # "YYYY-MM-DD HH:MM:SS"

def _load_creds() -> Credentials:
    """
    Load credentials from token.json, refresh if expired, and only fall back
    to browser consent if we truly don't have a valid token.
    """
    creds = None

    # 1) Load saved token if present
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # 2) Refresh silently if expired and we have a refresh token
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception:
            creds = None  # will trigger interactive flow below

    # 3) First-time or broken token: run interactive flow once
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
        # Opens a local browser once; after that, refresh is silent
        creds = flow.run_local_server(port=0, prompt="consent")

    # 4) Persist the (possibly refreshed/new) token
    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())

    return creds

def _svc():
    creds = _load_creds()
    return build("drive", "v3", credentials=creds, cache_discovery=False)

_filename_re = re.compile(r"[^A-Za-z0-9]+")
def _clean_part(s: str) -> str:
    s = _filename_re.sub("_", s.strip())
    return re.sub(r"_+", "_", s).strip("_")

def list_in_folder(folder_id: str) -> List[DriveFile]:
    try:
        service = _svc()
        q = f"'{folder_id}' in parents and trashed = false"
        fields = "files(id, name, size, modifiedTime)"
        resp = service.files().list(q=q, fields=fields, orderBy="modifiedTime desc").execute()
    except RefreshError as e:
        raise RuntimeError("Google auth failed. Delete token.json and re-run auth.") from e

    items = resp.get("files", [])
    out: List[DriveFile] = []
    for it in items:
        size_kb = int(int(it.get("size", 0)) / 1024) if it.get("size") else 0
        mtime = it["modifiedTime"].replace("T", " ").replace("Z", "")
        out.append(DriveFile(id=it["id"], name=it["name"], size_kb=size_kb, mtime=mtime))
    return out

# def create_text_file(folder_id: str, company: str, title: str, normalized_title: str, description: str) -> DriveFile:
#     service = _svc()
#     date_str = datetime.now().strftime("%m_%d_%y")
#     filename = f"{_clean_part(company)}_{_clean_part(title)}_{date_str}.txt"
#     body = (
#         f"Company: {company}\n"
#         f"Title: {title}\n\n"
#         f"Normalized Title: {normalized_title}\n\n"
#         "****************\n"
#         "Description:\n"
#         f"{description}\n"
#     )
#     meta = {"name": filename, "parents": [folder_id]}
#     media = MediaIoBaseUpload(io.BytesIO(body.encode("utf-8")), mimetype="text/plain")
#     created = service.files().create(body=meta, media_body=media, fields="id, name, size, modifiedTime").execute()
#     size_kb = int(int(created.get("size", 0)) / 1024) if created.get("size") else 0
#     mtime = created["modifiedTime"].replace("T", " ").replace("Z", "")
#     return DriveFile(id=created["id"], name=created["name"], size_kb=size_kb, mtime=mtime)

def create_json_file(folder_id: str,
                     company: str,
                     title_raw: str,
                     normalized_title: str,
                     description: str,
                     posted_at: str,
                     sheet_id: str) -> DriveFile:
    service = _svc()
    date_str = datetime.now().strftime("%m_%d_%y")
    filename = f"{_clean_part(company)}_{_clean_part(title_raw)}_{date_str}.json"

    payload = {
        "company": company,
        "title_raw": title_raw,
        "normalized_title": normalized_title,
        "description": description,
        "posted_at": posted_at,
        "filename_or_id": "",  # could be filled by n8n or later in pipeline
        "skills": [],
        "sheet_id": sheet_id
    }

    media = MediaIoBaseUpload(
        io.BytesIO(json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")),
        mimetype="application/json"
    )
    meta = {"name": filename, "parents": [folder_id]}

    created = service.files().create(
        body=meta,
        media_body=media,
        fields="id, name, size, modifiedTime"
    ).execute()

    size_kb = int(int(created.get("size", 0)) / 1024) if created.get("size") else 0
    mtime = created["modifiedTime"].replace("T", " ").replace("Z", "")
    return DriveFile(id=created["id"], name=created["name"], size_kb=size_kb, mtime=mtime)



def move_file(file_id: str, to_folder_id: str) -> None:
    service = _svc()
    file = service.files().get(fileId=file_id, fields="parents").execute()
    prev = ",".join(file.get("parents", []))
    service.files().update(fileId=file_id, addParents=to_folder_id, removeParents=prev, fields="id,parents").execute()
