from faker import Faker

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.tests.factories import UserFactory
from users.serializers import UsersSerializer

fake = Faker()


class UsersPrivateTests(APITestCase):
    """Tests user endpoint logged as normal user."""

    def setUp(self):
        self.user = UserFactory(last_name='Smith')
        self.user_2 = UserFactory(last_name='Jones')
        self.user_3 = UserFactory(last_name='Williams')
        self.client = APIClient()
        refresh_token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_token.access_token}')

    def test_get_list_of_users(self):
        url = reverse('user-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), get_user_model().objects.count())
        # Test order of users (last name)
        users = get_user_model().objects.all().order_by('last_name', 'first_name')
        serializer = UsersSerializer(users, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UsersSerializer(self.user)
        self.assertEqual(response.data, serializer.data)

    def test_create_user(self):
        url = reverse('user-list')
        user_count = get_user_model().objects.count()
        data = {
            'email': 'test@test.com',
            'password': fake.password(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), user_count+1)
        self.assertTrue(get_user_model().objects.filter(email=response.data.get('email')).exists())
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertNotIn('password', response.data)

    def test_create_user_with_existing_email_fail(self):
        url = reverse('user-list')
        data = {
            'email': self.user.email,
            'password': fake.password(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'user with this email already exists',
            response.data.get('errors')[0]['detail']
        )
        self.assertEqual(get_user_model().objects.count(), 3)

    def test_create_user_with_existing_email_case_insensitive_fail(self):
        url = reverse('user-list')
        data = {
            'email': self.user.email.upper(),
            'password': fake.password(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'user with this email already exists',
            response.data.get('errors')[0]['detail']
        )
        self.assertEqual(get_user_model().objects.count(), 3)

    def test_update_your_own_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])

    def test_update_your_own_user_password(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        data = {'password': fake.password()}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(data['password']))

    def test_update_your_own_user_with_existing_email_fail(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        data = {
            'email': self.user_2.email,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'user with this email already exists',
            response.data.get('errors')[0]['detail']
        )
        user_email = self.user.email
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, user_email)

    def test_update_your_own_user_with_existing_email_case_insensitive_fail(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        data = {
            'email': self.user_2.email.upper(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'user with this email already exists',
            response.data.get('errors')[0]['detail']
        )
        user_email = self.user.email
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, user_email)

    def test_update_other_user_is_forbiden(self):
        url = reverse('user-detail', kwargs={'pk': self.user_2.pk})
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user_email = self.user_2.email
        self.user_2.refresh_from_db()
        self.assertEqual(self.user_2.email, user_email)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'You do not have permission to perform this action.'
        )

    def test_delete_your_own_user_is_forbiden(self):
        users_count = get_user_model().objects.count()
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(get_user_model().objects.count(), users_count)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'You haven\'t permission to delete this object.'
        )

    def test_delete_other_user_is_forbiden(self):
        users_count = get_user_model().objects.count()
        url = reverse('user-detail', kwargs={'pk': self.user_2.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(get_user_model().objects.count(), users_count)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'You do not have permission to perform this action.'
        )


class UsersPrivateAdminTests(APITestCase):
    """Tests user endpoint logged as admin user."""

    def setUp(self):
        self.user = UserFactory(last_name='Smith', is_staff=True)
        self.user_2 = UserFactory(last_name='Jones')
        self.user_3 = UserFactory(last_name='Williams')
        self.client = APIClient()
        refresh_token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_token.access_token}')

    def test_update_other_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user_2.pk})
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])

    def test_delete_other_user(self):
        users_count = get_user_model().objects.count()
        url = reverse('user-detail', kwargs={'pk': self.user_2.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.count(), users_count-1)

    def test_delete_your_own_user(self):
        users_count = get_user_model().objects.count()
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.count(), users_count-1)


class UsersPublicTests(APITestCase):
    """Tests user endpoint without login."""

    def setUp(self):
        self.user = UserFactory(last_name='Smith', is_staff=True)
        self.user_2 = UserFactory(last_name='Jones')
        self.user_3 = UserFactory(last_name='Williams')
        self.client = APIClient()

    def test_get_users_list_is_forbiden(self):
        url = reverse('user-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'Authentication credentials were not provided.'
        )

    def test_get_user_detail_is_forbiden(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'Authentication credentials were not provided.'
        )

    def test_create_user_is_forbiden(self):
        url = reverse('user-list')
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'Authentication credentials were not provided.'
        )

    def test_update_user_is_forbiden(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'Authentication credentials were not provided.'
        )

    def test_delete_user_is_forbiden(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'Authentication credentials were not provided.'
        )
