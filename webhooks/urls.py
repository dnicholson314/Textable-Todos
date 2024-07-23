from django.urls import path
from . import views

urlpatterns = [
    path('', views.textable_todos_discord_bot_webhook),
    path('oauth2', views.receive_discord_auth, name="receive_discord_auth"),
]