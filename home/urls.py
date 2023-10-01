from django.urls import path
from . import views
from .views import send_message

urlpatterns = [
    path('', views.Home.as_view(), name='main'),
    path('contactus', send_message, name='contactus'),

]
