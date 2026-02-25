# Credential Rotation & Revocation

These steps help you rotate exposed Google OAuth credentials and tokens.

1. Revoke existing OAuth tokens (for safety)
   - Go to Google Account > Security > Manage third-party access and remove the app tokens, or
   - Use the OAuth token revocation endpoint for each refresh token:
     ```bash
     curl -d "token=<REFRESH_TOKEN>" -H "Content-type: application/x-www-form-urlencoded" -X POST https://oauth2.googleapis.com/revoke
     ```

2. Recreate OAuth Client ID
   - Open Google Cloud Console -> APIs & Services -> Credentials
   - Delete the compromised OAuth Client ID (or create a new one and restrict usage)
   - Create a new "Desktop" OAuth client or whichever type is appropriate
   - Download the new `credentials.json` and *do not commit it to git*

3. Update your environment
   - On local machine: update `.env` (gitignored) or export `GOOGLE_CLIENT_SECRETS_JSON` / `GOOGLE_TOKEN_JSON`
   - On VPS or CI: store `GEMINI_API_KEY`, and Google secrets in the platform's secret store (e.g., GitHub Secrets, systemd environment, or cloud secret manager)

4. Regenerate tokens locally
   - Run `python main.py` locally to perform the OAuth flow and generate new `token_*.json` files
   - Do not commit these token files. Transfer them to your VPS securely if needed, or configure your VPS to generate tokens there via a secure browser session or by using headless OAuth alternatives.

5. Monitor & audit
   - Check GitHub Security -> Secret scanning and remove any unblocked findings by rotating credentials.
   - Rotate any other keys that were exposed (Gemini/API keys, service account keys, etc.)

If you'd like, I can:
- Draft the exact curl commands and a short PowerShell script to revoke the refresh tokens you have.
- Help create GitHub Actions secrets and a simple deploy workflow that injects environment variables on the VPS.
