from __future__ import annotations

from datetime import date, timedelta

from django.contrib import messages
from django.db import OperationalError, transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from ..activitylog.middleware import log_activity
from ..settings import VERSION
from .models import OffboardingRecord


def _get_context_base() -> dict[str, str]:
    return {"version": VERSION}


def offboarding_list(request: HttpRequest) -> HttpResponse:
    queryset = OffboardingRecord.objects.all()
    try:
        records = list(queryset)
    except OperationalError:
        messages.error(
            request,
            "Looks like migrations haven’t been applied. Run scripts\\FIX_MIGRATIONS.bat.",
        )
        return render(
            request,
            "offboarding/list.html",
            {"records": [], **_get_context_base(), "seed_url": reverse("offboarding:seed")},
        )

    if not records:
        messages.info(request, "No offboarding records yet. Seed demo data!")

    log_activity(
        app="offboarding",
        action="LIST",
        request=request,
        extra={"count": len(records)},
    )
    return render(
        request,
        "offboarding/list.html",
        {"records": records, **_get_context_base(), "seed_url": reverse("offboarding:seed")},
    )


def offboarding_detail(request: HttpRequest, pk: int) -> HttpResponse:
    record = get_object_or_404(OffboardingRecord, pk=pk)
    log_activity(
        app="offboarding",
        action="DETAIL",
        request=request,
        extra={"record_id": record.pk},
    )
    return render(
        request,
        "offboarding/detail.html",
        {"record": record, **_get_context_base(), "list_url": reverse("offboarding:list")},
    )


@transaction.atomic
def offboarding_seed(request: HttpRequest) -> HttpResponse:
    today = date.today()
    demo_records = [
        {
            "developer_email": "maria.perez@example.com",
            "project": "Helios",
            "offboard_date": today - timedelta(days=10),
            "reason": "Contract completed",
            "handover_complete": True,
            "notes": "All assets archived.",
        },
        {
            "developer_email": "jacob.mills@example.com",
            "project": "Apollo",
            "offboard_date": today + timedelta(days=5),
            "reason": "Transition to vendor team",
            "handover_complete": False,
        },
        {
            "developer_email": "emma.cho@example.com",
            "project": "Nova",
            "offboard_date": today + timedelta(days=12),
            "reason": "Team consolidation",
            "handover_complete": False,
            "notes": "Pending credentials cleanup.",
        },
        {
            "developer_email": "tyler.nguyen@example.com",
            "project": "Mercury",
            "offboard_date": today - timedelta(days=3),
            "reason": "Performance improvement plan",
            "handover_complete": True,
        },
        {
            "developer_email": "sophia.garcia@example.com",
            "project": "Gemini",
            "offboard_date": today + timedelta(days=21),
            "reason": "Joining design org",
            "handover_complete": False,
        },
    ]
    OffboardingRecord.objects.bulk_create(
        OffboardingRecord(**record_data) for record_data in demo_records
    )

    log_activity(
        app="offboarding",
        action="SEED",
        request=request,
        extra={"count": len(demo_records)},
    )

    messages.success(request, "Demo offboarding records created.")
    return render(
        request,
        "offboarding/seeded.html",
        {"list_url": reverse("offboarding:list"), **_get_context_base()},
    )
