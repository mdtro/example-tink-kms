from django.urls import path
from . import views

urlpatterns = [
    path("save-token/", views.save_token, name="save_token"),
    path("success/", views.success, name="success"),
    path("view-tokens/", views.view_tokens, name="view_tokens"),
]
