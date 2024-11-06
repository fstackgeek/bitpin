from django.urls import path

from app.views import LoginView, PostsView, SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup-page'),
    path('login/', LoginView.as_view(), name='login-page'),
    path('', PostsView.as_view(), name='posts-page'),
]
