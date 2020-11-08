from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='alldoc_index'),
    path('fuel/as', views.fuel_as_management, name='alldoc_fuel_as_management'),
    path('fuel/supply', views.fuel_supply_management, name='alldoc_fuel_supply_management'),
    path('fuel/supply/delete/<int:pk>', views.fuel_supply_delete, name='alldoc_fuel_supply_delete'),
    path('fuel/auto/delete/<int:pk>', views.fuel_auto_delete, name='alldoc_fuel_auto_delete'),
    path('fuel/station/delete/<int:pk>', views.fuel_station_delete, name='alldoc_fuel_station_delete'),
    path('fuel/stat', views.fuel_stat, name='alldoc_fuel_stat'),
    path('pool/pool', views.pool_management, name='alldoc_pool_management'),
    path('pool/pool/delete/<int:pk>', views.pool_delete, name='alldoc_pool_delete'),
    path('pool/session', views.pool_session_management, name='alldoc_pool_session'),
    path('pool/session/delete/<int:pk>', views.pool_session_delete, name='alldoc_pool_session_delete'),
    path('pool/stat', views.pool_stat, name='alldoc_pool_stat'),
]