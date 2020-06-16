from django.shortcuts import redirect, render
from django.http import HttpResponse
from . import forms, models

# Create your views here.
def index(request):
    return render(request, 'alldoc/index.html')


def fuel_as_management(request):
    '''
    Auto & Station management: see, add and modify
    '''
    common = {"name": "Fuel"}

    # Form
    print(request)
    if request.method == 'POST' and 'auto-name' in request.POST:
        form_auto = forms.AutoForm(request.POST, prefix='auto')
        if form_auto.is_valid():
            form_auto.save()
            # ToDo: Redirect with GET
            # redirect('alldoc_fuel_as_management')
    else:
        form_auto = forms.AutoForm(prefix='auto')
    if request.method == 'POST' and 'station-name' in request.POST:
        form_station = forms.StationForm(request.POST, prefix='station')
        if form_station.is_valid():
            form_station.save()
    else:
        form_station = forms.StationForm(prefix='station')

    # Get data
    Auto = models.Auto.objects.all()
    Station = models.Station.objects.all()

    return render(request, 'alldoc/fuel_as_management.html', {"common": common, "Auto": Auto, "Station": Station,
                                                "AutoForm": form_auto, "StationForm": form_station})

