from rest_framework.routers import SimpleRouter

from .views.users import UsersView


router = SimpleRouter()
router.register(r'', UsersView)
urlpatterns = router.urls
