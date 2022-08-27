from faker import Faker

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.tests.factories import UserFactory
from services.tests.factories import BrandFactory
from services.models import Brand
from services.serializers import BrandSerializer

fake = Faker()


class BrandsPrivateTests(APITestCase):
    """Tests brands endpoint logged as normal user."""

    def setUp(self):
        self.user = UserFactory()
        self.brand = BrandFactory(name='Ford')
        self.brand_2 = BrandFactory(name='Volkswagen')
        self.brand_3 = BrandFactory(name='Fiat')
        self.client = APIClient()
        refresh_token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_token.access_token}')

    def test_list_brands(self):
        url = reverse('brand-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), Brand.objects.count())
        serializer = BrandSerializer(Brand.objects.all().order_by('name'), many=True)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_list_brands_with_searching(self):
        url = reverse('brand-list')
        params = {'search': self.brand_2.name}
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BrandSerializer(Brand.objects.filter(name=self.brand_2.name), many=True)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_list_brands_with_ordering(self):
        url = reverse('brand-list')
        params = {'ordering': 'name'}
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        brands = Brand.objects.all().order_by('name')
        serializer = BrandSerializer(brands, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)

        params = {'ordering': '-name'}
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        brands = brands.order_by('-name')
        serializer = BrandSerializer(brands, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_brand(self):
        url = reverse('brand-detail', kwargs={'pk': self.brand.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.brand.name)

    def test_get_brand_with_wrong_id_fail(self):
        url = reverse('brand-detail', kwargs={'pk': -1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('errors')[0]['detail'], 'Not found.')

    def test_create_brand(self):
        url = reverse('brand-list')
        brands_count = Brand.objects.count()
        data = {'name': fake.company()}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Brand.objects.count(), brands_count+1)
        self.assertTrue(Brand.objects.filter(name=response.data.get('name')).exists())
        self.assertEqual(response.data['name'], data['name'])

    def test_create_brand_with_existing_name_fail(self):
        url = reverse('brand-list')
        data = {'name': self.brand_2.name}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'brand with this name already exists',
            response.data.get('errors')[0]['detail']
        )
        self.assertEqual(Brand.objects.count(), 3)

    def test_create_brand_with_existing_name_case_insensitive_fail(self):
        url = reverse('brand-list')
        data = {'name': self.brand.name.upper()}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'brand with this name already exists',
            response.data.get('errors')[0]['detail']
        )
        self.assertEqual(Brand.objects.count(), 3)

    def test_update_brand(self):
        url = reverse('brand-detail', kwargs={'pk': self.brand.pk})
        data = {'name': fake.company()}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_update_brand_with_existing_name_fail(self):
        url = reverse('brand-detail', kwargs={'pk': self.brand.pk})
        data = {'name': self.brand_2.name}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'brand with this name already exists',
            response.data.get('errors')[0]['detail']
        )
        brand_name = self.brand.name
        self.brand.refresh_from_db()
        self.assertEqual(self.brand.name, brand_name)

    def test_delete_brand_is_forbiden(self):
        brand_count = Brand.objects.count()
        url = reverse('brand-detail', kwargs={'pk': self.brand.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Brand.objects.count(), brand_count)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'You haven\'t permission to delete this object.'
        )


class BrandsPrivateAdminTests(APITestCase):
    """Tests brands endpoint logged as admin user."""

    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.brand = BrandFactory()
        self.client = APIClient()
        refresh_token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_token.access_token}')

    def test_delete_brand(self):
        brand_count = Brand.objects.count()
        url = reverse('brand-detail', kwargs={'pk': self.brand.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Brand.objects.count(), brand_count-1)


class BrandsPublicTests(APITestCase):
    """Tests brands endpoint without login."""

    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.brand = BrandFactory()
        self.brand_2 = BrandFactory()
        self.brand_3 = BrandFactory()
        self.client = APIClient()

    def test_list_brands_is_forbiden(self):
        url = reverse('brand-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'Authentication credentials were not provided.'
        )

    def test_get_brand_is_forbiden(self):
        url = reverse('brand-detail', kwargs={'pk': self.brand.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'Authentication credentials were not provided.'
        )

    def test_create_brand_is_forbiden(self):
        url = reverse('brand-list')
        data = {'name': fake.company()}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'Authentication credentials were not provided.'
        )

    def test_update_brand_is_forbiden(self):
        url = reverse('brand-detail', kwargs={'pk': self.brand.pk})
        data = {'name': fake.company()}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'Authentication credentials were not provided.'
        )

    def test_delete_brand_is_forbiden(self):
        url = reverse('brand-detail', kwargs={'pk': self.brand.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('errors')[0]['detail'],
            'Authentication credentials were not provided.'
        )
