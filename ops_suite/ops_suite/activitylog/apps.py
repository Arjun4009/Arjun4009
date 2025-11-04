from django.apps import AppConfig


class ActivitylogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ops_suite.activitylog"
    label = "activitylog"
    verbose_name = "Activity Log"
