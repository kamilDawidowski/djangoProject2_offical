from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_old, name='index_old'),  # nic " "
    path('dowSp/', views.dowSp, name="dowSp"),
    path('genWyk/', views.genWyk, name="genWyk"),

]
