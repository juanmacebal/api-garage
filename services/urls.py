from rest_framework.routers import SimpleRouter

from services.views import services, vehicle_types, brands, vehicles, clients


router = SimpleRouter()
router.register(r'clients', clients.ClientsView)
router.register(r'brands', brands.BrandsView)
router.register(r'types', vehicle_types.VehicleTypesView)
router.register(r'vehicles', vehicles.VehiclesView)
router.register(r'services', services.ServicesView)
urlpatterns = router.urls
