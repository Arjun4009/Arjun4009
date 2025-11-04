from __future__ import annotations

from django.db import models


class OffboardingRecord(models.Model):
    developer_email = models.CharField(max_length=256, db_index=True)
    project = models.CharField(max_length=256)
    offboard_date = models.DateField()
    reason = models.TextField(null=True, blank=True)
    handover_complete = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-offboard_date"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.developer_email} ({self.project})"
