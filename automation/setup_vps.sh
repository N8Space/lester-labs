#!/bin/bash
set -e

# Navigate to dir
cd "$(dirname "$0")"
echo "Setting up Automation in $(pwd)..."

# 1. Install Python/Pip if missing (Debian/Ubuntu assumed)
# 1. Install Python/Pip/Venv
# Ensure venv is installed even if python3 is present
apt-get update && apt-get install -y python3 python3-pip python3-venv

# 2. Setup Venv
# If venv is missing or broken (no pip), recreate it
if [ ! -f "venv/bin/pip" ]; then
    echo "Creating virtual environment..."
    rm -rf venv
    python3 -m venv venv
fi

# 3. Install Requirements
./venv/bin/pip install -r requirements.txt

# 4. Setup Cron Job (Daily at 7:15am)
# Current Cron
crontab -l > mycron 2>/dev/null || true
# Remove existing entry to prevent duplicates
sed -i '/main.py/d' mycron
# Add new entry
echo "15 7 * * * cd $(pwd) && ./venv/bin/python main.py >> cron.log 2>&1" >> mycron
# Install
crontab mycron
rm mycron

echo "Cron job scheduled for 7:15 AM daily."
echo "You can check logs at $(pwd)/cron.log"
