from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt import views as jwt_views


@extend_schema(tags=['Token'])
class TokenObtainPairView(jwt_views.TokenObtainPairView):
    pass


@extend_schema(tags=['Token'])
class TokenRefreshView(jwt_views.TokenRefreshView):
    pass
