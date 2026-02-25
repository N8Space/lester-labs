$VPS_USER = "root"
$VPS_HOST = "72.62.175.6" # EDIT THIS
$REMOTE_DIR = "/root/automation"

Write-Host "Deploying to $VPS_USER@$VPS_HOST..."

# 1. Create remote directory
ssh $VPS_USER@$VPS_HOST "mkdir -p $REMOTE_DIR"

# 2. Copy files
# We confirm sending sensitive files (token_*.json, .env) so it works out of the box
scp main.py requirements.txt credentials.json token_*.json .env setup_vps.sh "${VPS_USER}@${VPS_HOST}:${REMOTE_DIR}"
scp -r src "${VPS_USER}@${VPS_HOST}:${REMOTE_DIR}"

Write-Host "Files transferred."
Write-Host "Now running setup script on VPS..."

# 3. Exec setup
ssh $VPS_USER@$VPS_HOST "chmod +x $REMOTE_DIR/setup_vps.sh && $REMOTE_DIR/setup_vps.sh"

Write-Host "Deployment Complete!"
