from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),  # admin
    path('api/', include('vendor_app.urls')),  # api
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),  # token
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),  # token
]
