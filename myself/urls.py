from django.urls import path
from . import views

urlpatterns = [
    path('<str:code>', views.index, name='myself_index'),
    path('', views.index, name='myself_index'),
]