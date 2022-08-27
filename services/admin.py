from django.contrib import admin

from services.models import Type, Brand, Vehicle, Service, Client


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'phone',
        'vehicles',
        'is_active',
    )
    search_fields = (
        'last_name',
        'first_name'
    )
    list_filter = ('is_active',)

    def vehicles(self, obj):
        return ', '.join([str(v) for v in obj.client_vehicles.all()])


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'brand',
        'model',
        'year',
        'color',
        'license_plate',
        'kilometers',
    )
    search_fields = (
        'brand__name',
        'model',
        'year',
        'color',
        'license_plate',
        'client__last_name',
        'client__first_name'
    )


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle',
        'client',
        'kilometers',
        'license_plate',
        'start_at',
        'finish_at',
        'is_paid',
    )
    search_fields = (
        'vehicle__brand__name',
        'vehicle__client__last_name',
        'vehicle__client__first_name',
        'vehicle__license_plate',
    )
    list_filter = (
        'is_paid',
    )

    def client(self, obj):
        return obj.vehicle.client

    def license_plate(self, obj):
        return obj.vehicle.license_plate


admin.site.register(Client, ClientAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Service, ServiceAdmin)
