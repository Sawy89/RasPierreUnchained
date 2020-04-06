from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import datetime
from . import forms, models
from django.contrib.auth.models import User


# %% Support Functions
def prepare_sidebar(current_user):
    '''
    Function for getting info for sidebar
    '''
    sidebar_data = {}
    
    sidebar_data['rooms'] = models.Room.objects.filter(end_date__gte=datetime.datetime.now()).all()   # Get available rooms
    sidebar_data['myrooms'] = models.Room.objects.filter(member=current_user).all()   # ToDO: add filter on user subscribed

    return sidebar_data


# %% Pages
@login_required
def index(request):
    # Get data for sidebar
    sidebar_data = prepare_sidebar(request.user)

    return render(request, 'xmasg/index.html', {"sidebar_data": sidebar_data}) 


@login_required
def room(request, pk):
    # Get room
    try:
        room = models.Room.objects.get(id=pk)
        room_members = room.member.all()
    except models.Room.DoesNotExist:
        raise Http404('Room does not exist')
    # Get form
    if request.user not in room_members:
        form = forms.RoomMemberForm()
        form.fields['user_id'].initial = request.user.id
        form.fields['room_id'].initial = room.id
    else:
        form = None
    # Get data for sidebar
    sidebar_data = prepare_sidebar(request.user)
    return render(request, 'xmasg/room.html', {"sidebar_data": sidebar_data, 
                                                "room": room, "room_members": room_members,
                                                "form_add_member": form}) 

@login_required
def room_add_member(request, room_id, user_id):
    '''
    Add a member to a room
    '''
    # Read form
    if request.method == 'GET':
        room = models.Room.objects.get(id=room_id)
        user = User.objects.get(id=user_id)
        room_members = room.member.all()
        if user not in room_members:
            room_member = models.RoomMember.objects.create(room=room, member=user, is_admin=False)
            room_member.save()
            return redirect('xmasg_room', pk=room.id)


@login_required
def room_new(request):
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            obj = form.save()
            room_member = models.RoomMember.objects.create(room=obj, member=request.user, is_admin=True)
            room_member.save()
            return redirect('xmasg_index')
    else:
        form = forms.RoomForm()
    # Get data for sidebar
    sidebar_data = prepare_sidebar(request.user)
    return render(request, 'xmasg/room_new.html', {"sidebar_data": sidebar_data,
                                                    "form": form}) 


# # %% API (Ajax)
# # @login_required
# def room_add_member(request):
#     '''
#     Add a member to a room
#     '''
#     if request.is_ajax and request.method == "POST":
#         form = forms.RoomMemberForm(request.POST)
#         if form.is_valid():
#             user1 = models.User.filter(id=form.user_id).first()
#             room1 = models.Room.filter(id=form.room_id).first()
#             room_member = models.RoomMember.objects.create(room=room1, 
#                                                             member=user1, is_admin=False)
#             room_member.save()
#             return JsonResponse({"alert_message": f"{user1.username} added to room {room1.name}"}, status=200)
#         else:
#             return JsonResponse({"alert_message": form.errors}, status=400)
#     return JsonResponse({"alert_message": "Wrong request"}, status=400)