CI Deploy workflow

This repository includes a GitHub Actions workflow to deploy to a VPS and a `systemd` service template.

Required GitHub Secrets (add under repo Settings → Secrets):

- `VPS_HOST` — server IP or hostname
- `VPS_USER` — SSH user (e.g., `root`)
- `VPS_SSH_PRIVATE_KEY` — private key for SSH (no passphrase or the runner must handle it)
- `GEMINI_API_KEY` — Google Gemini API key
- `GOOGLE_CLIENT_SECRETS_JSON` — (optional) full client_secrets JSON string for Google OAuth
- `GOOGLE_TOKEN_JSON` — (optional) pre-generated token JSON for the app

How it works:
1. Push to `main` triggers the workflow.
2. The runner creates `deploy.tar.gz` excluding local secret files.
3. Runner builds a small `.env.deploy` from GitHub Secrets and copies it plus the artifact to the VPS.
4. On the VPS the artifact is extracted to `/root/automation`, `/etc/automation/.env` is written with strict permissions, requirements are installed into `/root/automation/venv`, and the `automation.service` unit (if present) is installed and restarted.

Security notes:
- Do not commit secret files. Keep `.gitignore` updated.
- Keep the private key used by `VPS_SSH_PRIVATE_KEY` restricted and rotate it if exposed.
- Prefer limiting the deploy SSH key to allow only the necessary actions (e.g., scp/ssh). Consider using a dedicated deploy user instead of `root`.

If you'd like, I can:
- Add an encrypted artifact storage step, or
- Replace direct SSH with an SSM-based deployment (AWS Systems Manager), or
- Create a two-step canary deploy (one host first, then others).

