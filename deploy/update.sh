#!/usr/bin/env bash
# Redeploy after you push changes:  ssh in, then  bash deploy/update.sh
set -euo pipefail
cd /var/www/portfolio
git pull
./venv/bin/pip install -r requirements.txt
./venv/bin/python manage.py migrate --noinput
./venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart gunicorn-portfolio
echo "Deployed."
