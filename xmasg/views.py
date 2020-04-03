from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms, models


@login_required
def index(request):
    return render(request, 'xmasg/index.html', {"rooms": models.Room.objects.all(), "friends": None}) 


@login_required
def room(request):
    return render(request, 'xmasg/room.html', {"rooms": models.Room.objects.all(), "friends": None}) 


@login_required
def room_new(request):
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('xmasg_index')
    else:
        form = forms.RoomForm()
    return render(request, 'xmasg/room_new.html', {"rooms": None, "friends": None,
                                                    "form": form}) 