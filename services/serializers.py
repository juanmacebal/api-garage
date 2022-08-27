from django.contrib.auth import get_user_model

from rest_framework import serializers

from services.models import Brand, Service, Type, Vehicle, Client


class ClientUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'full_name']


class ClientsSerializer(serializers.ModelSerializer):
    created_by = ClientUserDetailsSerializer()

    class Meta:
        model = Client
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

    def validate_name(self, name):
        brands = Brand.objects.filter(name__iexact=name)
        if self.instance:
            brands = brands.exclude(pk=self.instance.pk)
        if brands.exists():
            raise serializers.ValidationError('brand with this name already exists.')
        return name


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class VehiclesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = '__all__'


class VehiclesResponseSerializer(serializers.ModelSerializer):
    client = ClientsSerializer()

    class Meta:
        model = Vehicle
        fields = '__all__'
        depth = 1


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class ServiceResponseSerializer(serializers.ModelSerializer):
    vehicle = VehiclesResponseSerializer()

    class Meta:
        model = Service
        fields = '__all__'
        depth = 1
