"""Fill the site with the content from Yash's resume. Safe to run more than once.

    python manage.py seed_portfolio          # only fills an empty site
    python manage.py seed_portfolio --reset  # wipes portfolio content and re-seeds
"""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Credential, Experience, Profile, Project, SkillGroup

SEED_DIR = Path(__file__).resolve().parent.parent.parent / "seed"

SUMMARY = (
    "I'm a Python backend developer with 3+ years of experience building scalable, secure, "
    "data-intensive web applications with Django, Django REST Framework and FastAPI. I design "
    "REST APIs, tune PostgreSQL and MySQL queries, run background work with Celery and Redis, "
    "and deploy on AWS with Docker and CI/CD.\n\n"
    "Most of my recent work is on IoT platforms: telemetry pipelines, webhooks and alerting over "
    "MQTT and InfluxDB. I care about APIs that stay fast under load, and code that ships with "
    "tests."
)

EXPERIENCE = [
    {
        "role": "Software Development Engineer",
        "company": "Onemind Services LLC",
        "location": "Gurugram, India",
        "period": "Aug 2024 – Sept 2026",
        "bullets": [
            "Engineered scalable webhook and alert systems for an IoT platform using Python, FastAPI, MQTT and InfluxDB, with asynchronous processing, modular architecture and robust error handling and logging, improving real-time communication by 40%.",
            "Built monitoring dashboards with Recharts and implemented background and scheduled tasks using Celery with Redis to process telemetry data, run alert checks and sync controller data.",
            "Worked in an Agile/Scrum team: daily stand-ups, sprint planning and retrospectives.",
        ],
    },
    {
        "role": "Junior Backend Developer",
        "company": "Sehaj Synergy Tech Pvt. Ltd.",
        "location": "Jaipur, India",
        "period": "Sept 2023 – Jul 2024",
        "bullets": [
            "Designed and developed RESTful APIs with Django REST Framework, migrating template-based views to scalable backend services and reducing latency by 25%.",
            "Integrated a payment gateway for prepaid water meter recharges and built the recharge processing and invoice generation based on prepaid usage.",
            "Optimized Django ORM queries and API endpoints to process and retrieve high-volume IoT data efficiently.",
            "Wrote 500+ Pytest unit tests with 100% coverage and kept work organised with Git workflows.",
        ],
    },
]

PROJECTS = [
    {
        "title": "Smart Water Metering Application",
        "tech": "Python, Django, Django REST Framework, PostgreSQL",
        "bullets": [
            "Prepaid smart water metering platform with real-time consumption monitoring and automated billing.",
            "Dashboard visualisation, automated invoice generation and household registration management.",
            "Normalised PostgreSQL schema built for high-frequency meter readings across many households, tuned for real-time usage tracking and billing queries.",
            "REST APIs with role-based access control (admin, household) to protect meter data and limit billing actions by role.",
        ],
    },
    {
        "title": "IoT Webhook and Alert System",
        "tech": "Python, FastAPI, MQTT, InfluxDB, Celery, Redis",
        "bullets": [
            "Webhook delivery and alerting for an IoT platform, built at Onemind Services.",
            "Asynchronous processing with Celery and Redis for telemetry ingestion, scheduled alert checks and controller sync.",
            "Monitoring dashboards in Recharts on top of the telemetry data.",
        ],
    },
]

SKILLS = [
    ("Languages", "Python, SQL, Bash, C++"),
    ("Frameworks and APIs", "Django, Django REST Framework, FastAPI, Flask, REST APIs, Webhooks, Microservices"),
    ("Databases and messaging", "PostgreSQL, MySQL, Redis, InfluxDB, Django ORM, Celery, MQTT"),
    ("Cloud and DevOps", "AWS (EC2, S3, Lambda), Docker, Linux, Git, GitHub Actions, CI/CD, Grafana, Prometheus"),
    ("Testing and AI", "Pytest, TDD, Agile/Scrum, LLMs, RAG, LangChain, Vector Databases"),
]

CREDENTIALS = [
    dict(kind="education", title="Bachelor of Technology",
         institution="Jaipur Engineering College and Research Center",
         period="Aug 2019 – Aug 2023", detail="CGPA 8.2"),
    dict(kind="certification", title="Develop Generative AI Applications: Get Started",
         institution="IBM (Coursera)"),
    dict(kind="certification", title="Django, FastAPI, Docker, GitHub Actions, Git & GitHub, Unit Testing & TDD",
         institution="Udemy"),
]


class Command(BaseCommand):
    help = "Seed the portfolio with content from the resume."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing content first.")

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            for model in (Profile, Experience, Project, SkillGroup, Credential):
                model.objects.all().delete()
        elif Profile.objects.exists():
            self.stdout.write("Portfolio already has content. Use --reset to overwrite it.")
            return

        github = "https://github.com/Yashjain18111"
        profile = Profile.objects.create(
            name="Yash Jain",
            headline="Python backend developer building APIs and real-time IoT systems.",
            summary=SUMMARY,
            location="Gurugram, India",
            email="yashjain18111@gmail.com",
            github_url=github,
            linkedin_url="https://www.linkedin.com/in/yashjain18111/",
        )
        resume = SEED_DIR / "resume.pdf"
        if resume.exists():
            with resume.open("rb") as fh:
                profile.resume.save("Yash_Jain_Resume.pdf", File(fh), save=True)

        for i, data in enumerate(EXPERIENCE):
            Experience.objects.create(order=i, **{**data, "bullets": "\n".join(data["bullets"])})

        for i, data in enumerate(PROJECTS):
            Project.objects.create(
                order=i,
                github_url=github if i == 0 else "",
                **{**data, "bullets": "\n".join(data["bullets"])},
            )

        for i, (name, items) in enumerate(SKILLS):
            SkillGroup.objects.create(name=name, items=items, order=i)

        for i, data in enumerate(CREDENTIALS):
            Credential.objects.create(order=i, **data)

        self.stdout.write(self.style.SUCCESS("Portfolio seeded."))
