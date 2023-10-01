from django.urls import path
from account import views

app_name = 'account'
urlpatterns = [
    path('login', views.UserLoginView.as_view(), name='user login'),
    path('register', views.OtpLoginView.as_view(), name='user register'),
    path('checkotp', views.CheckOtpView.as_view(), name='check otp'),
    path('logout', views.user_logout, name='log out'),
    path('edit', views.edit_profile, name='Edit profile'),
    path('add/address', views.AddAddressView.as_view(), name='add_address'),
    # path('edit', views.EditProfileView.as_view(), name='Edit profile'),

]
