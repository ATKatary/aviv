"""
LLM url patterns
"""
from llm import views
from django.urls import path, re_path

urlpatterns = [
    path("logEvent", views.log_event, name="log_event"),
    path("getAiMessage", views.get_ai_message, name="get_ai_message"),
]
