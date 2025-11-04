from __future__ import annotations

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class ActivityLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="activity_logs",
    )
    path = models.CharField(max_length=512)
    method = models.CharField(max_length=8)
    remote_addr = models.CharField(max_length=64, null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    app = models.CharField(max_length=64)
    action = models.CharField(max_length=128)
    extra = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Activity Log Entry"
        verbose_name_plural = "Activity Log Entries"

    def __str__(self) -> str:  # pragma: no cover - human readable representation
        username = None
        if self.user_id:
            User = get_user_model()
            try:
                username = User.objects.only("username").get(pk=self.user_id).username
            except User.DoesNotExist:
                username = None
        return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {username or 'anonymous'} {self.method} {self.path}"
