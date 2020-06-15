from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='alldoc_index'),
    path('fuel/as', views.fuel_as_management, name='alldoc_fuel_as_management'),
]