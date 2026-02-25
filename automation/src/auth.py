import os
import json
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def authenticate_google_services(client_secret_file='credentials.json', token_file='token.json'):
    """Authenticate with Google APIs.

    This function supports reading client secrets and tokens from environment
    variables to avoid storing secrets in repository files. Supported env vars:

    - `GOOGLE_CLIENT_SECRETS_JSON`: full client_secrets JSON (preferred)
    - `GOOGLE_CLIENT_SECRET_FILE`: path to client secrets file
    - `GOOGLE_TOKEN_JSON`: full token JSON (optional)
    - `GOOGLE_TOKEN_FILE`: path to token file to read/write (optional)

    If env vars are not provided, falls back to the legacy file-based behavior.
    """

    creds = None

    # Try token from env var first
    token_json_env = os.getenv('GOOGLE_TOKEN_JSON')
    token_file_env = os.getenv('GOOGLE_TOKEN_FILE')
    if token_json_env:
        try:
            info = json.loads(token_json_env)
            creds = Credentials.from_authorized_user_info(info, SCOPES)
        except Exception:
            creds = None

    # Try token file (env-specified or default)
    if not creds:
        tf = token_file_env or token_file
        if tf and os.path.exists(tf):
            creds = Credentials.from_authorized_user_file(tf, SCOPES)

    # If there are no (valid) credentials available, run auth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # First try client secrets from env var
            client_secrets_env = os.getenv('GOOGLE_CLIENT_SECRETS_JSON')
            client_secret_file_env = os.getenv('GOOGLE_CLIENT_SECRET_FILE')
            if client_secrets_env:
                client_config = json.loads(client_secrets_env)
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            else:
                cs_file = client_secret_file_env or client_secret_file
                if not os.path.exists(cs_file):
                    raise FileNotFoundError(f"Client secrets file '{cs_file}' not found. Provide it or set GOOGLE_CLIENT_SECRETS_JSON in the environment.")
                flow = InstalledAppFlow.from_client_secrets_file(cs_file, SCOPES)

            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run if a writable file path is available
        save_path = token_file_env or token_file
        if save_path:
            with open(save_path, 'w') as token:
                token.write(creds.to_json())

    return creds
