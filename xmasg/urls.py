from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='xmasg_index'),
    path('room/<int:pk>', views.room, name='xmasg_room'),
    path('room/addmember', views.room_add_member, name='xmasg_room_add_member'),
    path('room/removemember', views.room_remove_member, name='xmasg_room_remove_member'),
    path('room/new', views.room_new, name='xmasg_room_new'),
    path('ajax/roommember/modification', views.RoomMemberModification.as_view(), name='xmasgajax_roommember_modification'),
    path('ajax/roomdate/modification', views.RoomDateModification.as_view(), name='xmasgajax_date_modification'),
]