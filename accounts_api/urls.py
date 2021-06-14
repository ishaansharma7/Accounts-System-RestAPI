from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('accounts.api.urls')),

    # make a post request with body containing email and password of only registered user
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # make a post request with body containing refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # make a post request with body containing access token with key being token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),    
]
