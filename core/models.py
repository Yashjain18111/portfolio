from django.db import models


def split_lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def split_commas(text):
    return [item.strip() for item in text.split(",") if item.strip()]


class Profile(models.Model):
    """The person the site is about. Only one row is used."""

    name = models.CharField(max_length=100)
    headline = models.CharField(max_length=200)
    summary = models.TextField(help_text="About section. Separate paragraphs with a blank line.")
    location = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    resume = models.FileField(upload_to="resume/", blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def paragraphs(self):
        return [p.strip() for p in self.summary.split("\n\n") if p.strip()]


class Experience(models.Model):
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100, blank=True)
    period = models.CharField(max_length=60, help_text='For example "Aug 2024 – Sept 2026"')
    bullets = models.TextField(help_text="One bullet per line.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.role} at {self.company}"

    @property
    def bullet_list(self):
        return split_lines(self.bullets)


class Project(models.Model):
    title = models.CharField(max_length=150)
    summary = models.CharField(max_length=300, blank=True)
    bullets = models.TextField(blank=True, help_text="One bullet per line.")
    tech = models.CharField(max_length=300, blank=True, help_text="Comma-separated.")
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def bullet_list(self):
        return split_lines(self.bullets)

    @property
    def tech_list(self):
        return split_commas(self.tech)


class SkillGroup(models.Model):
    name = models.CharField(max_length=100)
    items = models.TextField(help_text="Comma-separated.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    @property
    def item_list(self):
        return split_commas(self.items)


class Credential(models.Model):
    class Kind(models.TextChoices):
        EDUCATION = "education", "Education"
        CERTIFICATION = "certification", "Certification"

    kind = models.CharField(max_length=20, choices=Kind.choices)
    title = models.CharField(max_length=200)
    institution = models.CharField(max_length=200, blank=True)
    period = models.CharField(max_length=60, blank=True)
    detail = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.created_at:%d %b %Y})"
