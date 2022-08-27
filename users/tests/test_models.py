from faker import Faker

from django.test import TestCase

from users.models import User


fake = Faker()


class UsersModelTests(TestCase):
    """Tests models of users app."""

    def setUp(self):
        self.user = User.objects.create(
            email=fake.email().upper(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        self.user.refresh_from_db()

    def test_user_model(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.full_name, f'{self.user.first_name} {self.user.last_name}')
        self.assertEqual(str(self.user), f'{self.user.full_name} - {self.user.email}')

    def test_user_model_email_always_is_lower_case(self):
        self.assertEqual(self.user.email, self.user.email.lower())

    def test_create_user(self):
        user = User.objects.create_user(
            email=fake.email(),
            password=fake.password(),
        )
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_active, True)

    def test_create_user_hash_password(self):
        password = fake.password()
        user = User.objects.create_user(
            email=fake.email(),
            password=password,
        )
        self.assertTrue(user.check_password(password))

    def test_create_user_with_existing_name_is_exception(self):
        self.assertRaises(Exception, User.objects.create, email=self.user.email)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email=fake.email(),
            password=fake.password(),
        )
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_active, True)

    def test_create_superuser_with_wrong_email_is_exception(self):
        self.assertRaises(
            Exception, User.objects.create_superuser, email='', password=fake.password()
        )

    def test_create_superuser_with_wrong_password_is_exception(self):
        self.assertRaises(Exception, User.objects.create_superuser, email=fake.email(), password='')
