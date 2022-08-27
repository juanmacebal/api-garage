from django.db import models
from django.contrib.auth import get_user_model


class Client(models.Model):
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        get_user_model(), related_name='clients', null=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.full_name}"


class Type(models.Model):
    name = models.CharField(max_length=100, help_text="Type of vehicle, e.g. Car, Truck, etc.")

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            help_text="Brand of vehicle, e.g. Ford, Fiat, etc.")

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    type = models.ForeignKey(Type, related_name='type_vehicles', on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, related_name='brand_vehicles', on_delete=models.PROTECT)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    color = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=10)
    kilometers = models.IntegerField()
    client = models.ForeignKey(Client, related_name='client_vehicles', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.brand} {self.model} ({self.year})'


class Service(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='vehicle_services', on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    finish_at = models.DateTimeField(null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)
    repairs = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    kilometers = models.IntegerField()

    def __str__(self):
        return f'{self.vehicle} {self.vehicle.client}'
