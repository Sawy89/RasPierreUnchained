from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
from . import forms, models


def prepare_sidebar(current_user):
    '''
    Function for getting info for sidebar
    '''
    sidebar_data = {}
    
    sidebar_data['rooms'] = models.Room.objects.filter(end_date__gte=datetime.datetime.now()).all()   # Get available rooms
    sidebar_data['myrooms'] = models.Room.objects.filter(member=current_user).all()   # ToDO: add filter on user subscribed

    return sidebar_data


@login_required
def index(request):
    # Get data for sidebar
    sidebar_data = prepare_sidebar(request.user)

    return render(request, 'xmasg/index.html', {"sidebar_data": sidebar_data}) 


@login_required
def room(request, pk):
    try:
        room = models.Room.objects.get(id=pk)
    except models.Room.DoesNotExist:
        raise Http404('Room does not exist')
    # Get data for sidebar
    sidebar_data = prepare_sidebar(request.user)
    return render(request, 'xmasg/room.html', {"sidebar_data": sidebar_data, "room": room}) 


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