from faker import Faker
from dateutil import tz

from django.test import TestCase

from users.tests.factories import UserFactory
from services.models import Brand, Client, Service, Type, Vehicle

fake = Faker()


class ServicesModelTests(TestCase):
    """Tests models of services app."""

    def setUp(self):
        self.user = UserFactory()
        self.client = Client.objects.create(
            is_active=True,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            company=fake.company(),
            email=fake.email(),
            phone=fake.phone_number()[:20],
            address=fake.address(),
            city=fake.city(),
            state=fake.state(),
        )
        self.vehicle_type = Type.objects.create(name='Car')
        self.vehicle_brand = Brand.objects.create(name='Ford')
        self.vehicle = Vehicle.objects.create(
            type=self.vehicle_type,
            brand=self.vehicle_brand,
            model='Ka',
            year='2000',
            color='red',
            license_plate='sdf-1234',
            kilometers=fake.random_int(min=0, max=100000),
            client=self.client
        )
        self.service = Service.objects.create(
            start_at=fake.date_time_this_year(tzinfo=tz.gettz('UTC')),
            vehicle=self.vehicle,
            kilometers=fake.random_int(min=0, max=100000),
        )

    def test_brand_model(self):
        self.assertTrue(isinstance(self.vehicle_brand, Brand))
        self.assertEqual(str(self.vehicle_brand), self.vehicle_brand.name)

    def test_vehicle_type_model(self):
        self.assertTrue(isinstance(self.vehicle_type, Type))
        self.assertEqual(str(self.vehicle_type), self.vehicle_type.name)

    def test_vehicle_model(self):
        self.assertTrue(isinstance(self.vehicle, Vehicle))
        self.assertEqual(
            str(self.vehicle),
            f'{self.vehicle.brand} {self.vehicle.model} ({self.vehicle.year})'
        )

    def test_service_model(self):
        self.assertTrue(isinstance(self.service, Service))
        self.assertEqual(str(self.service), f'{self.vehicle} {self.vehicle.client}')

    def test_client_model(self):
        self.assertTrue(isinstance(self.client, Client))
        self.assertEqual(self.client.full_name, f'{self.client.first_name} {self.client.last_name}')
        self.assertEqual(str(self.client), self.client.full_name)
