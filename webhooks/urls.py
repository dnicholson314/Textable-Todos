from django.urls import path
from . import views

urlpatterns = [
    path('', views.discord_bot_webhook),
    path('oauth2', views.discord_auth_webhook, name="receive_discord_auth"),
]