from django.contrib import admin

from .models import ContactMessage, Credential, Experience, Profile, Project, SkillGroup


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "headline", "email")

    def has_add_permission(self, request):
        # The site shows a single profile; edit the existing one instead of adding more.
        return not Profile.objects.exists()


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "period", "order")
    list_editable = ("order",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "tech", "order")
    list_editable = ("order",)


@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "institution", "order")
    list_editable = ("order",)
    list_filter = ("kind",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_read")
    list_filter = ("is_read",)
    list_editable = ("is_read",)
    readonly_fields = ("name", "email", "message", "created_at")
    search_fields = ("name", "email", "message")

    def has_add_permission(self, request):
        return False
