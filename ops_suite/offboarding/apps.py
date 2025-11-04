from django.apps import AppConfig


class OffboardingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ops_suite.offboarding"
    label = "offboarding"
    verbose_name = "Offboarding Management"
