from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import Credential, Experience, Profile, Project, SkillGroup


def _page(request, form, status=200):
    credentials = Credential.objects.all()
    context = {
        "profile": Profile.objects.first(),
        "experiences": Experience.objects.all(),
        "projects": Project.objects.all(),
        "skill_groups": SkillGroup.objects.all(),
        "education": [c for c in credentials if c.kind == Credential.Kind.EDUCATION],
        "certifications": [c for c in credentials if c.kind == Credential.Kind.CERTIFICATION],
        "form": form,
    }
    return render(request, "core/home.html", context, status=status)


def home(request):
    return _page(request, ContactForm())


@require_POST
def contact(request):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return _page(request, form, status=400)

    if not form.cleaned_data["website"]:  # honeypot empty -> real visitor
        form.save()
    messages.success(request, "Thanks, your message was sent. I'll reply by email.")
    return redirect(reverse("home") + "#contact")


def healthz(request):
    """Used by uptime checks / load balancers."""
    return HttpResponse("ok", content_type="text/plain")
