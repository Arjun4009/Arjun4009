from django.urls import path

from . import views

app_name = "offboarding"

urlpatterns = [
    path("", views.offboarding_list, name="list"),
    path("<int:pk>/", views.offboarding_detail, name="detail"),
    path("seed/", views.offboarding_seed, name="seed"),
]
