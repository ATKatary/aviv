"""
User url patterns
"""
from user import views
from django.urls import path, re_path

urlpatterns = [
    path("create", views.create_user, name="create_user"),
]
