# Email Automation (GTD & Daily Digest)

This Python tool automates your inbox using the **Getting Things Done (GTD)** methodology + **Google Gemini AI**.

## Updates (Feb 2026)
*   **Multi-Account Support**: Checks `nslpublishing@gmail.com` and `Nathan.scott.lester@gmail.com`.
*   **Calendar & Tasks**: Integrates daily schedule and tasks from the primary account.
*   **Timezone Aware**: Configured for `America/Chicago` (CST/CDT) regardless of server location.
*   **Auto-Cleanup**: Archives (>30 days) and Trashes (>8 years) old emails.

## Setup Instructions

### 1. Environment Setup
1.  Ensure Python is installed.
2.  Open a terminal in this folder (`automation/`).
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure Environment Variables:
    *   Copy `.env.example` to a new file named `.env`.
    *   Edit `.env`:
        *   `GEMINI_API_KEY`: Paste your key from [Google AI Studio](https://aistudio.google.com/app/apikey).
        *   `EMAIL_ADDRESS`: (Optional, used as fallback).

### 2. Google Cloud Credentials (Important!)
To access your Gmail and Tasks, you need an OAuth Client ID.

You can provide credentials either via environment variables (recommended) or a local file.

Option A — Environment variables (recommended):

1.  Set `GOOGLE_CLIENT_SECRETS_JSON` to the full client_secrets JSON content from Google Cloud (paste the JSON string).
2.  Optionally set `GOOGLE_TOKEN_JSON` to a previously-generated token JSON, or set `GOOGLE_TOKEN_FILE` to a path where the token should be stored (ensure that path is gitignored).
3.  Add your email(s) as "Test Users" in the OAuth Consent Screen.

Option B — File-based (legacy):

1.  Enable **Gmail API**, **Google Tasks API**, and **Google Calendar API**.
2.  Create **OAuth Desktop App** credentials.
3.  Download and save the client secrets as `credentials.json` in this folder (or set `GOOGLE_CLIENT_SECRET_FILE` to another path).
4.  Add your email(s) as "Test Users" in the OAuth Consent Screen.

## Running the Script
### 1. Local Authentication (Required First Time)
Run the script locally to generate the necessary token files (`token_nsl.json` and `token_nathan.json`):
```bash
python main.py
```
*   **First Run**: A browser window will open asking you to log in. You will likely need to log in **twice** (once for each account).
    *   First prompt: Log in as `nslpublishing@gmail.com`.
    *   Second prompt: Log in as `Nathan.scott.lester@gmail.com`.
*   **Note**: The script is set to `DRY_RUN = True` by default so it won't delete anything yet.

### 2. Deployment to VPS
Once tokens are generated locally:
1.  **Edit `deploy_vps.ps1`** with your VPS IP.
2.  **Run Deployment**:
    ```powershell
    .\deploy_vps.ps1
    ```
    This copies your code *and* the generated token files to the VPS.
3.  **Verify**: SSH into your VPS and check `/root/automation/cron.log`.

## Customization
*   **Timezone**: `USER_TIMEZONE` in `main.py` is set to 'America/Chicago'.
*   **Dry Run**: Change `DRY_RUN = False` in `main.py` to enable actual emailing, archiving, and trashing.
