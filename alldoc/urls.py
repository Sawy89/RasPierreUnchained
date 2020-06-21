from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='alldoc_index'),
    path('fuel/as', views.fuel_as_management, name='alldoc_fuel_as_management'),
    path('fuel/supply', views.fuel_supply_management, name='alldoc_fuel_supply_management'),
    path('fuel/supply/delete/<int:pk>', views.fuel_supply_delete, name='alldoc_fuel_supply_delete'),
]