$VPS_USER = "root"
$VPS_HOST = "72.62.175.6" # EDIT THIS
$REMOTE_DIR = "/root/automation"

Write-Host "Deploying to $VPS_USER@$VPS_HOST..."

# 1. Create remote directory
ssh $VPS_USER@$VPS_HOST "mkdir -p $REMOTE_DIR"

# 2. Copy files
# By default we DO NOT copy local secret files (credentials.json, token_*.json, .env).
# If you explicitly want to include them, set $INCLUDE_SECRETS = $true below.
$INCLUDE_SECRETS = $false

if ($INCLUDE_SECRETS) {
	Write-Host "Including secret files in deploy (credentials, token_*.json, .env)"
	scp main.py requirements.txt credentials.json token_*.json .env setup_vps.sh "${VPS_USER}@${VPS_HOST}:${REMOTE_DIR}"
} else {
	Write-Host "Deploying without local secret files. Upload secrets separately to the VPS environment."
	scp main.py requirements.txt setup_vps.sh "${VPS_USER}@${VPS_HOST}:${REMOTE_DIR}"
}
scp -r src "${VPS_USER}@${VPS_HOST}:${REMOTE_DIR}"

Write-Host "Files transferred."
Write-Host "Now running setup script on VPS..."

# 3. Exec setup
ssh $VPS_USER@$VPS_HOST "chmod +x $REMOTE_DIR/setup_vps.sh && $REMOTE_DIR/setup_vps.sh"

Write-Host "Deployment Complete!"
