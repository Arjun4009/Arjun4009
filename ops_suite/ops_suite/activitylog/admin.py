from django.contrib import admin

from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "app", "action", "status_code", "path", "method")
    list_filter = ("app", "action", "status_code", "timestamp")
    search_fields = ("path", "user__username", "app", "action", "remote_addr")
    readonly_fields = tuple(field.name for field in ActivityLog._meta.get_fields())
    ordering = ("-timestamp",)
    list_per_page = 25
