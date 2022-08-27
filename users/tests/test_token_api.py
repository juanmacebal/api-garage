from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class TokenPublicTests(APITestCase):
    """Tests for token endpoint to obtein a token pair."""

    def setUp(self):
        self.user_data = {
            'email': 'test@test.com',
            'password': 'test',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.client = APIClient()

    def test_get_access_token_with_valid_credentials(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_access_token_with_wrong_password_is_unauthorized(self):
        url = reverse('token_obtain_pair')
        data = self.user_data.copy()
        data['password'] = 'wrong'
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('errors', response.data)
        self.assertIn(
            'No active account found with the given credentials',
            response.data.get('errors')[0]['detail']
        )

    def test_get_access_token_with_wrong_email_is_unauthorized(self):
        url = reverse('token_obtain_pair')
        data = self.user_data.copy()
        data['email'] = 'wrong@email.com'
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(
            'No active account found with the given credentials',
            response.data.get('errors')[0]['detail']
        )

    def test_get_access_token_with_invalid_credentials_is_unauthorized(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'wrong@email.com',
            'password': 'wrong',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(
            'No active account found with the given credentials',
            response.data.get('errors')[0]['detail']
        )


class TokenRefreshPublicTests(APITestCase):
    """Tests for refresh token endpoint."""

    def setUp(self):
        self.user_data = {
            'email': 'test@test.com',
            'password': 'test',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.client = APIClient()
        self.tokens = self.client.post(
            reverse('token_obtain_pair'),
            self.user_data
        )

    def test_get_refresh_token_with_valid_token(self):
        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh': self.tokens.data['refresh']})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_get_refresh_token_with_invalid_token_is_unauthorized(self):
        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh': 'invalid'})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('errors', response.data)
        self.assertIn(
            'Token is invalid',
            response.data.get('errors')[0]['detail']
        )
