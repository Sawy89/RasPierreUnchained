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
    for auto in Auto:
        auto.deletable = True if not(auto.supply.all().exists()) else False 
    Station = models.Station.objects.all()
    for station in Station:
        station.deletable = True if not(station.supply.all().exists()) else False

    return render(request, 'alldoc/fuel_as_management.html', {"common": common, "Auto": Auto, "Station": Station,
                                                "AutoForm": form_auto, "StationForm": form_station})


def fuel_supply_management(request):
    '''
    Supply management
    '''
    common = {"name": "Fuel"}

    # Form
    print(request)
    if request.method == 'POST':
        form = forms.SupplyForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        last_auto = models.Supply.objects.latest('id').auto if models.Supply.objects.all() else None
        last_station = models.Supply.objects.latest('id').station if models.Supply.objects.all() else None
        last_distance = models.Supply.objects.latest('id').distance_total if models.Supply.objects.all() else None
        form = forms.SupplyForm(initial={'auto':last_auto, 'station':last_station, 'distance_total':last_distance})

    # Get data
    diz_supply = {}
    for auto in models.Auto.objects.all():
        Supply = models.Supply.objects.filter(auto=auto).order_by('event_date').all()#[::-1][:10][::-1]     # only last elements
        for supply_id, supply in enumerate(Supply):
            supply.deletable = True if supply_id+1 == len(Supply) else False
        diz_supply[auto.name] = Supply

    return render(request, 'alldoc/fuel_supply_management.html', {"common": common, "Auto": diz_supply, "SupplyForm": form})


def fuel_supply_delete(request, pk):
    '''Delete supply'''
    if request.method == 'POST':
        models.Supply.objects.filter(pk=pk).delete()
    return redirect('alldoc_fuel_supply_management')


def fuel_auto_delete(request, pk):
    '''Delete auto'''
    if request.method == 'POST':
        models.Auto.objects.filter(pk=pk).delete()
    return redirect('alldoc_fuel_as_management', permanent=True)


def fuel_station_delete(request, pk):
    '''Delete station'''
    if request.method == 'POST':
        models.Station.objects.filter(pk=pk).delete()
    return redirect('alldoc_fuel_as_management')


def fuel_stat(request):
    Supply = models.Supply.objects.all()
    return render(request, 'alldoc/fuel_stat.html', {"Supply": Supply})