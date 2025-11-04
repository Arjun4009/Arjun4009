from __future__ import annotations

from django.db import models


class TransitionSheet(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - human friendly
        return self.name


class TransitionRow(models.Model):
    sheet = models.ForeignKey(
        TransitionSheet,
        related_name="rows",
        on_delete=models.CASCADE,
    )
    developer_email = models.CharField(max_length=256, db_index=True)
    previous_project = models.CharField(max_length=256, null=True, blank=True)
    new_project = models.CharField(max_length=256)
    effective_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    receiving_manager = models.CharField(max_length=256, null=True, blank=True)
    reference = models.CharField(max_length=256, null=True, blank=True)
    email_sent = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["developer_email"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.developer_email} -> {self.new_project}"
