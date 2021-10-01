from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *
from .forms import UserLoginForm

app_name = 'farmer'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(form_class=UserLoginForm), name='login'),
    # path('logout/', loginview, name='logout'),
    path('register/', FarmerRegisterView.as_view(), name='register'),
    path('profile/', FarmerProfileView.as_view(), name='profile'),
    path('edit-profile<str:user>/', EditProfileView.as_view(), name='edit-profile'),
]
