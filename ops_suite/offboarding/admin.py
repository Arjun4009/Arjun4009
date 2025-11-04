from django.contrib import admin

from .models import OffboardingRecord


@admin.register(OffboardingRecord)
class OffboardingRecordAdmin(admin.ModelAdmin):
    list_display = ("developer_email", "project", "offboard_date", "handover_complete")
    list_filter = ("handover_complete", "offboard_date")
    search_fields = ("developer_email", "project")
    ordering = ("-offboard_date",)
