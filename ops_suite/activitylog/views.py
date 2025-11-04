from __future__ import annotations

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..settings import VERSION
from .models import ActivityLog


def logs_list(request: HttpRequest) -> HttpResponse:
    queryset = ActivityLog.objects.select_related("user").order_by("-timestamp")
    app_filter = request.GET.get("app")
    action_filter = request.GET.get("action")
    search = request.GET.get("q")

    if app_filter:
        queryset = queryset.filter(app=app_filter)
    if action_filter:
        queryset = queryset.filter(action=action_filter)
    if search:
        queryset = queryset.filter(
            Q(path__icontains=search)
            | Q(user__username__icontains=search)
            | Q(remote_addr__icontains=search)
        )

    paginator = Paginator(queryset, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "activitylog/list.html",
        {
            "page_obj": page_obj,
            "filters": {
                "app": app_filter or "",
                "action": action_filter or "",
                "q": search or "",
            },
            "version": VERSION,
        },
    )
