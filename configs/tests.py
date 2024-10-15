from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Config
from urllib import parse
from todo.settings import DISCORD_APPLICATION_ID
from unittest.mock import patch
from .views import URL_PARAMS

import uuid

USERNAME = 'testuser'
DISCORD_USERNAME="test_discord_username"
PASSWORD = "12345"
SETTINGS_URL = reverse('user_settings')
AUTH_URL = reverse('initiate_discord_auth')
MOCK_UUID = "12345678123456781234567812345678"
EXPECTED_STATE = "12345678-1234-5678-1234-567812345678"

class SettingsUrlTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)

    def test_settings_url_loads_when_logged_in(self):
        """
        Tests whether the settings url loads when the user is logged in.
        """
        self.client.login(username=USERNAME, password=PASSWORD)

        response = self.client.get(SETTINGS_URL)

        # Check if the 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'configs/settings.html')

    def test_settings_url_redirects_when_logged_out(self):
        """
        Tests whether the settings url redirects to the login page if the user is not logged in.
        """
        response = self.client.get(SETTINGS_URL)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_settings_url_shows_discord_username_with_config(self):
        """
        Tests whether the settings url shows the user's discord username if they have one.
        """
        self.client.login(username=USERNAME, password=PASSWORD)
        Config.objects.create(
            user=self.user, 
            discord_username=DISCORD_USERNAME
        )

        response = self.client.get(SETTINGS_URL)
        self.assertEqual(response.context['discord_username'], DISCORD_USERNAME)

    def test_settings_url_shows_blank_with_no_config(self):
        """
        Tests whether the settings url is empty if the user does not have a config object.
        """

        self.client.login(username=USERNAME, password=PASSWORD)

        response = self.client.get(SETTINGS_URL)
        self.assertEqual(response.context['discord_username'], '')

class DiscordAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)

    def test_auth_url_redirects_to_login_when_logged_out(self):
        """
        Tests whether the Discord authentication URL redirects to the login page if the user is logged out.
        """

        response = self.client.get(AUTH_URL)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    @patch('uuid.uuid4')
    def test_auth_url_redirects_to_discord_with_params_when_logged_in(self, mock_uuid):
        """
        Tests whether the Discord authentication URL redirects to Discord's OAuth2 portal with the correct parameters if the user is logged in.
        """
        mock_uuid.return_value = uuid.UUID(MOCK_UUID)
        self.client.login(username=USERNAME, password=PASSWORD)

        response = self.client.get(AUTH_URL)
        self.assertEqual(response.status_code, 302)

        params = URL_PARAMS
        params["state"] = EXPECTED_STATE
        params["redirect_url"] = reverse('receive_discord_auth')
        url_encoded_params = parse.urlencode(params)

        self.assertIn(url_encoded_params, response.url)

    def test_auth_url_sends_session_state(self):
        """
        Tests whether the Discord authentication URL properly stores and handles state.
        """
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(AUTH_URL)

        self.assertEqual(response.status_code, 302)
        self.assertIn('oauth2_state', self.client.session)

        state = self.client.session['oauth2_state']
        self.assertIn(f'state={state}', response.url)