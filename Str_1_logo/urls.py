from django.urls import path
from . import views

urlpatterns = [
    path('', views.logo, name='logo'),#nic " "


]
