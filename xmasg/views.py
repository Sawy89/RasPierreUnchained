from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'xmasg/index.html') 


@login_required
def room(request):
    return render(request, 'xmasg/room.html', {"rooms": None, "friends": None}) 


@login_required
def room_new(request):
    return render(request, 'xmasg/room_new.html', {"rooms": None, "friends": None}) 