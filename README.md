# Yash Jain: portfolio site

A Django portfolio with the same layout as the `django-ecom` reference: a project package
(`portfolio/`), one app (`core/`) with `models.py`, `views.py`, `admin.py`, templates under
`core/templates/core/`, SQLite by default, and a `media/` folder for uploads.

All content (about text, jobs, projects, skills, resume PDF) lives in the database and is
edited at `/admin/`. Contact-form messages land there too.

```
portfolio-site/
├── manage.py
├── requirements.txt
├── .env.example
├── portfolio/            settings, urls, wsgi
├── core/
│   ├── models.py         Profile, Experience, Project, SkillGroup, Credential, ContactMessage
│   ├── views.py  urls.py  forms.py  admin.py  tests.py
│   ├── management/commands/seed_portfolio.py   loads your resume content
│   ├── templates/core/   base.html, home.html
│   ├── static/core/      css/style.css, js/main.js
│   └── seed/resume.pdf
└── deploy/               gunicorn + nginx config, setup and update scripts
```

## Run it locally

```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                  # then set DJANGO_SECRET_KEY
python manage.py migrate
python manage.py seed_portfolio                       # loads your resume content
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/admin/. Run the tests with `python manage.py test`.

## Deploy on AWS (EC2 + nginx + gunicorn + free HTTPS)

A t3.micro (or t2.micro) is plenty. Pick the **Asia Pacific (Mumbai) ap-south-1** region for low latency from India.

**1. Launch the instance**
- EC2 → Launch instance → **Ubuntu Server 24.04 LTS**, t3.micro, create/download a key pair.
- Security group inbound rules: SSH (22) from *your IP only*, HTTP (80) and HTTPS (443) from anywhere.
- Allocate an **Elastic IP** and attach it to the instance, so the address survives reboots.

**2. Point your domain at it**
At your domain registrar (or Route 53) add `A` records for `yourdomain.com` and `www.yourdomain.com` → the Elastic IP.

**3. Get the code onto the server**
Push this project to a GitHub repo first, then:

```bash
ssh -i your-key.pem ubuntu@<elastic-ip>
sudo mkdir -p /var/www/portfolio && sudo chown ubuntu:ubuntu /var/www/portfolio
git clone https://github.com/Yashjain18111/<your-repo>.git /var/www/portfolio
cd /var/www/portfolio
```

**4. Create `.env`**
```bash
cp .env.example .env
python3 -c "import secrets; print(secrets.token_urlsafe(50))"   # use this as DJANGO_SECRET_KEY
nano .env
```
Set:
```
DJANGO_SECRET_KEY=<the generated value>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DJANGO_HTTPS=False          # switch to True in step 7
```

**5. Run the setup script**
```bash
bash deploy/setup_ec2.sh yourdomain.com
```
It installs nginx and certbot, builds the virtualenv, migrates, collects static files, loads your
resume content, and starts gunicorn under systemd.

**6. Create your admin user**
```bash
cd /var/www/portfolio && ./venv/bin/python manage.py createsuperuser
```

**7. Turn on HTTPS**
Once the domain resolves to the server:
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```
Then set `DJANGO_HTTPS=True` in `.env` and run `sudo systemctl restart gunicorn-portfolio`.
Certbot renews the certificate automatically.

**Updating later:** push to GitHub, SSH in, run `bash deploy/update.sh`.

### Troubleshooting
- `sudo journalctl -u gunicorn-portfolio -n 50` shows app errors; `sudo tail /var/log/nginx/error.log` shows nginx errors.
- 400 "Bad Request": the domain is missing from `DJANGO_ALLOWED_HOSTS`.
- CSRF error on the contact form after enabling HTTPS: check `DJANGO_CSRF_TRUSTED_ORIGINS` includes the `https://` origins.
- 502 Bad Gateway: gunicorn isn't running; check the journal command above.

## Editing content
Sign in at `/admin/`. Add projects (with a screenshot and GitHub/live links), reorder anything with the
`order` number, and replace the resume PDF on the Profile page. Contact messages appear under
"Contact messages".

## Notes
- Your phone number is deliberately not on the site (public pages get scraped); the email is.
- The seeded "Smart Water Metering Application" links to your GitHub profile. Edit it in the admin
  to point at the real repo, and add your other GitHub projects there.
- Optional: set the `DB_*` variables in `.env` to use PostgreSQL instead of SQLite.
  SQLite is fine for a portfolio; back up `db.sqlite3` and `media/` if you use it.
