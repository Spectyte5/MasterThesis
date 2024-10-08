"""
Definition of urls for MasterThesis.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from app import forms, views


urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path(
        "login/",
        LoginView.as_view(
            template_name="app/login.html",
            authentication_form=forms.BootstrapAuthenticationForm,
            extra_context={
                "title": "Log in",
                "year": datetime.now().year,
            },
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("admin/", admin.site.urls),
    path("app/", views.app, name="app"),
    path("validation/", views.validation, name="validation"),
    path("save_configuration/", views.save_configuration, name="save_configuration"),
    path(
        "load_configuration/<str:config_name>/",
        views.load_configuration,
        name="load_configuration",
    ),
    path(
        "list_custom_configurations/",
        views.list_custom_configurations,
        name="list_custom_configurations",
    ),
     path('delete_configuration/<str:config_name>/', 
          views.delete_configuration, 
          name='delete_configuration'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
