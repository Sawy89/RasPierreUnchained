from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import datetime
import math
from . import forms, models
from django.contrib.auth.models import User
from string import Template


# %% Support Functions
def prepare_sidebar(current_user):
    '''
    Function for getting info for sidebar
    '''
    sidebar_data = {}
    
    sidebar_data['rooms'] = models.Room.objects.filter(end_date__gte=datetime.datetime.now()).exclude(member=current_user).all()   # Get available rooms
    sidebar_data['myrooms'] = models.Room.objects.filter(member=current_user).all()   # ToDO: add filter on user subscribed

    return sidebar_data


class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


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
        room.end_date_str = room.end_date.strftime('%d-%m-%Y %H:%M')
        delta = room.end_date.replace(tzinfo=None) - datetime.datetime.now()
        room.end_date_delta_str = strfdelta(delta, "%D giorni, %H ore %M minuti e %S secondi!")
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
def room_add_member(request):
    '''
    Add a member to a room
    '''
    # Read form
    if request.method == 'POST':
        form = forms.RoomMemberForm(request.POST)
        if form.is_valid():
            room = models.Room.objects.get(id=form.cleaned_data['room_id'])
            user = User.objects.get(id=form.cleaned_data['user_id'])
            room_members = room.member.all()
            if user not in room_members:
                room_member = models.RoomMember.objects.create(room=room, member=user, is_admin=False)
                room_member.save()
            return redirect('xmasg_room', pk=room.id)
    return HttpResponseBadRequest('Wrong add member request')


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
