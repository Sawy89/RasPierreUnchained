from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='xmasg_index'),
    path('room/<int:pk>', views.room, name='xmasg_room'),
    path('room/new', views.room_new, name='xmasg_room_new'),
]