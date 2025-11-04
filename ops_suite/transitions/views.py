from __future__ import annotations

from datetime import date, timedelta

from django.contrib import messages
from django.db import OperationalError, transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from ..activitylog.middleware import log_activity
from ..settings import VERSION
from .models import TransitionRow, TransitionSheet


def _get_context_base() -> dict[str, str]:
    return {"version": VERSION}


def transitions_list(request: HttpRequest) -> HttpResponse:
    queryset = TransitionSheet.objects.prefetch_related("rows")
    try:
        sheets = list(queryset)
    except OperationalError:
        messages.error(
            request,
            "Looks like migrations haven’t been applied. Run scripts\\FIX_MIGRATIONS.bat.",
        )
        return render(request, "transitions/list.html", {"sheets": [], **_get_context_base()})

    if not sheets:
        messages.info(request, "No transition sheets yet. Seed some demo data!")

    log_activity(
        app="transitions",
        action="LIST",
        request=request,
        extra={"count": len(sheets)},
    )
    return render(request, "transitions/list.html", {"sheets": sheets, **_get_context_base()})


def transitions_detail(request: HttpRequest, pk: int) -> HttpResponse:
    sheet = get_object_or_404(TransitionSheet.objects.prefetch_related("rows"), pk=pk)
    log_activity(
        app="transitions",
        action="DETAIL",
        request=request,
        extra={"sheet_id": sheet.pk, "count": sheet.rows.count()},
    )
    return render(request, "transitions/detail.html", {"sheet": sheet, **_get_context_base()})


@transaction.atomic
def transitions_seed(request: HttpRequest) -> HttpResponse:
    today = date.today()
    sheet = TransitionSheet.objects.create(name=f"Demo Transition Sheet {today:%Y-%m-%d %H:%M:%S}")

    demo_rows = [
        {
            "developer_email": "alex.jones@example.com",
            "previous_project": "Mercury",
            "new_project": "Apollo",
            "effective_date": today + timedelta(days=7),
            "end_date": today + timedelta(days=90),
            "receiving_manager": "Dana Carver",
            "reference": "TR-1001",
            "email_sent": True,
            "notes": "All access transferred.",
        },
        {
            "developer_email": "samira.khan@example.com",
            "previous_project": "Orion",
            "new_project": "Gemini",
            "effective_date": today + timedelta(days=14),
            "receiving_manager": "Louise Becker",
            "reference": "TR-1002",
            "email_sent": False,
            "notes": "Pending documentation.",
        },
        {
            "developer_email": "li.wei@example.com",
            "previous_project": "Gemini",
            "new_project": "Helios",
            "effective_date": today + timedelta(days=30),
            "receiving_manager": "Chris Archer",
            "reference": "TR-1003",
            "email_sent": True,
            "notes": "Security review complete.",
        },
        {
            "developer_email": "nora.iverson@example.com",
            "previous_project": "Helios",
            "new_project": "Luna",
            "effective_date": today + timedelta(days=21),
            "end_date": today + timedelta(days=180),
            "receiving_manager": "Pat Singh",
            "email_sent": False,
            "notes": "Backfill contract pending.",
        },
        {
            "developer_email": "diego.ramirez@example.com",
            "previous_project": "Apollo",
            "new_project": "Nova",
            "effective_date": today + timedelta(days=5),
            "receiving_manager": "Chris Archer",
            "reference": "TR-1005",
            "email_sent": True,
        },
    ]
    TransitionRow.objects.bulk_create(
        TransitionRow(sheet=sheet, **row_data) for row_data in demo_rows
    )

    log_activity(
        app="transitions",
        action="SEED",
        request=request,
        extra={"sheet_id": sheet.pk, "count": len(demo_rows)},
    )

    messages.success(request, "Demo transition sheet created.")
    return render(
        request,
        "transitions/seeded.html",
        {"sheet": sheet, "list_url": reverse("transitions:list"), **_get_context_base()},
    )
