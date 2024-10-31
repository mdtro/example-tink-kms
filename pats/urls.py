from django.urls import path
from . import views

urlpatterns = [
    path("save-token/", views.save_token, name="save_token"),
]
