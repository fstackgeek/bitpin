from authentication.views import SignUpView, TestSignUpBulkUsersView
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/test/bulksignup/', TestSignUpBulkUsersView.as_view(), name='test-bulk-signup'),
    path('api/', include('blog.urls')),
    path('', include('app.urls')),
]
