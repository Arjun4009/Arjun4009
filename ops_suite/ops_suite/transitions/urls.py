from django.urls import path

from . import views

app_name = "transitions"

urlpatterns = [
    path("", views.transitions_list, name="list"),
    path("<int:pk>/", views.transitions_detail, name="detail"),
    path("seed/", views.transitions_seed, name="seed"),
]
