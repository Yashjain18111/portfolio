from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, Profile


class PortfolioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_portfolio", verbosity=0)

    def test_home_renders_profile_content(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yash Jain")
        self.assertContains(response, "Smart Water Metering Application")
        self.assertContains(response, "Onemind Services LLC")

    def test_seed_is_idempotent(self):
        call_command("seed_portfolio", verbosity=0)
        self.assertEqual(Profile.objects.count(), 1)

    def test_contact_saves_message(self):
        response = self.client.post(reverse("contact"), {
            "name": "Asha", "email": "asha@example.com", "message": "Hello there",
        })
        self.assertRedirects(response, reverse("home") + "#contact", fetch_redirect_response=False)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_contact_honeypot_is_dropped(self):
        self.client.post(reverse("contact"), {
            "name": "Bot", "email": "bot@example.com", "message": "spam", "website": "http://spam",
        })
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_invalid_shows_errors(self):
        response = self.client.post(reverse("contact"), {"name": "", "email": "nope", "message": ""})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "data-has-errors", status_code=400)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_rejects_get(self):
        self.assertEqual(self.client.get(reverse("contact")).status_code, 405)

    def test_healthz(self):
        self.assertEqual(self.client.get(reverse("healthz")).content, b"ok")
