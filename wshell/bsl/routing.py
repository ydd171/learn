# chat/routing.py
from django.urls import re_path

from . import run_job

websocket_urlpatterns = [
    re_path(r'bsl/run_job/$', run_job.ChatConsumer),
]