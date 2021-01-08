from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('odp/', views.odp, name="odp"),
    path('odp/odp', views.odp, name="odp"),
    path('odp2', views.odp2, name="odp2"),
    path('odp/odp2', views.odp2, name="odp2"),
    path('odp/menu', views.menu, name="menu"),

]
