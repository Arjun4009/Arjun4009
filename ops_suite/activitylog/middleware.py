from __future__ import annotations

from collections.abc import Callable
from typing import Any

from django.http import HttpRequest, HttpResponse

from .models import ActivityLog


EXCLUDED_PREFIXES = ("/static/", "/favicon.ico")


def _should_skip(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in EXCLUDED_PREFIXES)


def get_remote_addr(request: HttpRequest) -> str | None:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class ActivityLogMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if _should_skip(request.path):
            return self.get_response(request)

        try:
            entry = ActivityLog.objects.create(
                path=request.path,
                method=request.method,
                user=request.user if request.user.is_authenticated else None,
                remote_addr=get_remote_addr(request),
                app="core",
                action=request.method,
            )
        except Exception:  # pragma: no cover - logging should never break requests
            return self.get_response(request)

        response = self.get_response(request)
        ActivityLog.objects.filter(pk=entry.pk).update(status_code=response.status_code)
        return response


def log_activity(*, app: str, action: str, request: HttpRequest, extra: dict[str, Any] | None = None) -> None:
    if _should_skip(request.path):
        return
    try:
        ActivityLog.objects.create(
            path=request.path,
            method=request.method,
            user=request.user if request.user.is_authenticated else None,
            remote_addr=get_remote_addr(request),
            status_code=None,
            app=app,
            action=action,
            extra=extra or {},
        )
    except Exception:  # pragma: no cover
        pass
