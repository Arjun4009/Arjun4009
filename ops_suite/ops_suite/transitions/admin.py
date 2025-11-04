from django.contrib import admin

from .models import TransitionRow, TransitionSheet


class TransitionRowInline(admin.TabularInline):
    model = TransitionRow
    extra = 0
    show_change_link = True


@admin.register(TransitionSheet)
class TransitionSheetAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name", "rows__developer_email", "rows__new_project")
    date_hierarchy = "created_at"
    inlines = [TransitionRowInline]


@admin.register(TransitionRow)
class TransitionRowAdmin(admin.ModelAdmin):
    list_display = (
        "developer_email",
        "new_project",
        "sheet",
        "receiving_manager",
        "effective_date",
        "end_date",
        "email_sent",
    )
    list_filter = ("receiving_manager", "effective_date", "end_date", "email_sent")
    search_fields = ("developer_email", "new_project", "receiving_manager", "reference")
    autocomplete_fields = ("sheet",)
