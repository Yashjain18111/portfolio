#!/usr/bin/env bash
# First-time setup on a fresh Ubuntu 24.04 EC2 instance.
#
#   1. Copy / clone this project to /var/www/portfolio (owned by ubuntu)
#   2. cp .env.example .env  and edit it (see README.md)
#   3. bash deploy/setup_ec2.sh yourdomain.com
#
# Re-running is safe.
set -euo pipefail

DOMAIN="${1:?Usage: bash deploy/setup_ec2.sh yourdomain.com}"
APP_DIR=/var/www/portfolio

cd "$APP_DIR"
[ -f .env ] || { echo "Missing $APP_DIR/.env. Copy .env.example to .env and edit it first."; exit 1; }
grep -q '^DJANGO_SECRET_KEY=change-me' .env && { echo "Set a real DJANGO_SECRET_KEY in .env first."; exit 1; }
chmod 600 .env

sudo apt-get update
sudo apt-get install -y python3-venv python3-pip nginx certbot python3-certbot-nginx

python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

mkdir -p media staticfiles
./venv/bin/python manage.py migrate --noinput
./venv/bin/python manage.py collectstatic --noinput
./venv/bin/python manage.py seed_portfolio   # only fills an empty site

sudo cp deploy/gunicorn-portfolio.service /etc/systemd/system/gunicorn-portfolio.service
sudo sed "s/__DOMAIN__/$DOMAIN/g" deploy/nginx-portfolio.conf | sudo tee /etc/nginx/sites-available/portfolio >/dev/null
sudo ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/portfolio
sudo rm -f /etc/nginx/sites-enabled/default

sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn-portfolio
sudo systemctl restart gunicorn-portfolio
sudo nginx -t
sudo systemctl reload nginx

echo
echo "Site is up on http://$DOMAIN (once DNS points at this server)."
echo "Next: create your admin user, then enable HTTPS. See README.md steps 6 and 7."
