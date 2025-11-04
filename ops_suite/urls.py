from django.contrib import admin
from django.urls import include, path

from . import views
from .activitylog import views as activitylog_views

urlpatterns = [
    path("", views.root_redirect, name="root"),
    path("health/", views.health, name="health"),
    path("admin/", admin.site.urls),
    path("transitions/", include("ops_suite.transitions.urls")),
    path("offboarding/", include("ops_suite.offboarding.urls")),
    path("logs/", activitylog_views.logs_list, name="logs"),
]
