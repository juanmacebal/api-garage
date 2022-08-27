from django.contrib.auth import get_user_model
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        exclude = ['groups', 'user_permissions', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
        read_only_fields = ['is_staff', 'is_superuser', 'last_login']

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
