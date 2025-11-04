from __future__ import annotations

from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect

from .settings import VERSION


def root_redirect(_: HttpRequest):
    return redirect("/transitions/")


def health(_: HttpRequest):
    return JsonResponse({"status": "ok", "version": VERSION})
