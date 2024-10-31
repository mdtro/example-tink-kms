from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("pats/", include("pats.urls"), name="pats"),
    path("", RedirectView.as_view(pattern_name="save_token", permanent=True)),
]
