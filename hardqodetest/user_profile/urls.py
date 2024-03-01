from django.urls import path
from .views import UserCreationApiView, SingIn, Logout


app_name = 'user_profile'

urlpatterns = [
    path('sign-up', UserCreationApiView.as_view(), name='sign-up'),
    path('sign-in', SingIn.as_view(), name='sign-in'),
    path('logout', Logout.as_view(), name='logout')
]