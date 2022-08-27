import factory

from factory.django import DjangoModelFactory

from services.models import Brand


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Faker('company')
