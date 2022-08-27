from rest_framework import serializers
from drf_spectacular.openapi import AutoSchema


class ErrorsSerializer(serializers.Serializer):
    code = serializers.CharField()
    detail = serializers.CharField()
    attr = serializers.CharField()


class GenericErrorSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=['validation_error', 'client_error', 'server_error'])
    errors = ErrorsSerializer(many=True)


class ValidationErrorSerializer(GenericErrorSerializer):
    pass


class UnauthenticatedErrorSerializer(GenericErrorSerializer):
    pass


class ForbiddenErrorSerializer(GenericErrorSerializer):
    pass


class NotFoundErrorSerializer(GenericErrorSerializer):
    pass


class AutoSchemaWithErrors(AutoSchema):
    def _get_response_bodies(self):
        response_bodies = super()._get_response_bodies()
        if len(list(filter(lambda _: _.startswith('4'), response_bodies.keys()))):
            return response_bodies

        add_error_codes = []
        if not self.method == 'GET':
            add_error_codes.append('400')

        if self.get_auth():
            add_error_codes.append('401')
            add_error_codes.append('403')

        if not (self.method == 'GET' and self._is_list_view()):
            if len(list(filter(lambda _: _['in'] == 'path', self._get_parameters()))):
                add_error_codes.append('404')

        self.error_response_bodies = {
            '400': self._get_response_for_code(ValidationErrorSerializer, '400'),
            '401': self._get_response_for_code(UnauthenticatedErrorSerializer, '401'),
            '403': self._get_response_for_code(ForbiddenErrorSerializer, '403'),
            '404': self._get_response_for_code(NotFoundErrorSerializer, '404')
        }
        for code in add_error_codes:
            response_bodies[code] = self.error_response_bodies[code]
        return response_bodies
