from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_config_general, name='user_settings'),
    path('authorize', views.initiate_discord_auth, name='initiate_discord_auth'),
]