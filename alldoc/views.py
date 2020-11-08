from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from highcharts import Highchart
import numpy as np
import json
from decimal import Decimal
import datetime
from django.utils import timezone

from . import forms, models


# %% Support
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

# %% Create your views here.
@staff_member_required
def index(request):
    return render(request, 'alldoc/index.html')


@staff_member_required
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


@staff_member_required
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
        Supply = models.Supply.objects.filter(auto=auto).order_by('event_date').all()[::-1][:10][::-1]     # only last elements
        for supply_id, supply in enumerate(Supply):
            supply.deletable = True if supply_id+1 == len(Supply) else False
        diz_supply[auto.name] = Supply

    return render(request, 'alldoc/fuel_supply_management.html', {"common": common, "Auto": diz_supply, "SupplyForm": form})


@staff_member_required
def fuel_supply_delete(request, pk):
    '''Delete supply'''
    if request.method == 'POST':
        models.Supply.objects.filter(pk=pk).delete()
    return redirect('alldoc_fuel_supply_management')


@staff_member_required
def fuel_auto_delete(request, pk):
    '''Delete auto'''
    if request.method == 'POST':
        models.Auto.objects.filter(pk=pk).delete()
    return redirect('alldoc_fuel_as_management', permanent=True)


@staff_member_required
def fuel_station_delete(request, pk):
    '''Delete station'''
    if request.method == 'POST':
        models.Station.objects.filter(pk=pk).delete()
    return redirect('alldoc_fuel_as_management')


@staff_member_required
def fuel_stat(request, auto_id=None, start_date=None, end_date=None):
    '''Stat for supply'''
    common = {"name": "Fuel"}

    # Initial-default values
    last_auto = models.Supply.objects.latest('id').auto
    start_date_init = timezone.now().date() + timezone.timedelta(days=-60)
    end_date_init = timezone.now().date()

    # get form
    form = forms.FuelStatForm(request.GET)
    if form.is_valid():
        common["auto"] = form.cleaned_data['auto']
        common["start_date"] = form.cleaned_data['start_date']
        common["end_date"] = form.cleaned_data['end_date']
    else:
        form = forms.FuelStatForm(initial={"auto":last_auto, "start_date":start_date_init,
                                "end_date":end_date_init})
        common["auto"] = last_auto
        common["start_date"] = start_date_init
        common["end_date"] = end_date_init 
    
    # Get data
    Supply = models.Supply.objects.filter(auto=common["auto"]).filter(event_date__gte=common["start_date"]) \
                        .filter(event_date__lte=common["end_date"]).order_by('event_date').all()
    cum_sum = [[0, 0, 0]] # calcolo la somma, per ottenere la cumulata  
    for supply in Supply:
        supply.calcStat()
        cum_sum.append([supply.event_date, cum_sum[-1][1]+supply.distance, cum_sum[-1][2]+supply.volume])
    cum_sum.pop(0)
    
    # Highchart
    chart = Highchart(height = 500)
    chart.add_data_set([[1000*(a.event_date-datetime.date(1970,1,1)).total_seconds(), int(a.pricevolume*100)/100] for a in Supply], series_type='line', name='Prezzo (€/litro)')
    chart.add_data_set([[1000*(a.event_date-datetime.date(1970,1,1)).total_seconds(), int(a.consumption1*100)/100] for a in Supply], series_type='line', name='km con un litro')
    chart.add_data_set([[1000*(a[0]-datetime.date(1970,1,1)).total_seconds(), int(a[1]/a[2]*100)/100] for a in cum_sum], series_type='line', name='km con un litro (tendenza)')
    
    chart.set_options('xAxis', {'type': 'datetime', 'gridLineWidth': 1})
#    chart.set_options('chart', {'backgroundColor':'transparent'})
    chart.set_options('tooltip', {'formatter': 'default_tooltip'})
    chart.set_options('title', {'text': f"Statistiche consumo {common['auto']}"})
    chart.htmlcontent;
    chart_dict = {"header": chart.htmlheader, "content":chart.content}

    return render(request, 'alldoc/fuel_stat.html', {"common": common, "Supply": Supply, "form": form, "chart": chart_dict})


# %% Pool
@staff_member_required
def pool_management(request):
    '''
    Pool: see, add and modify
    '''
    common = {"name": "Pool"}

    # Form
    print(request)
    if request.method == 'POST':
        form_pool = forms.PoolForm(request.POST, prefix='pool')
        if form_pool.is_valid():
            form_pool.save()
            # ToDo: Redirect with GET
            # redirect('alldoc_fuel_as_management')
    else:
        form_pool = forms.PoolForm(prefix='pool')
    
    # Get data
    Pool = models.Pool.objects.all()
    for pool in Pool:
        pool.deletable = True if not(pool.session.all().exists()) else False 

    return render(request, 'alldoc/pool_management.html', {"common": common, "Pool": Pool,
                                                "PoolForm": form_pool})



@staff_member_required
def pool_delete(request, pk):
    '''Delete pool'''
    if request.method == 'POST':
        models.Pool.objects.filter(pk=pk).delete()
    return redirect('alldoc_pool_management', permanent=True)


@staff_member_required
def pool_session_management(request):
    '''
    Pool session management
    '''
    common = {"name": "Pool"}

    # Form
    print(request)
    if request.method == 'POST':
        form = forms.PoolSessionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        last_pool = models.PoolSession.objects.latest('id').pool if models.PoolSession.objects.all() else None
        last_lap_number = models.PoolSession.objects.latest('id').lap_number if models.PoolSession.objects.all() else None
        form = forms.PoolSessionForm(initial={'pool':last_pool, 'lap_number':last_lap_number})

    # Get data
    PoolSession = models.PoolSession.objects.order_by('-event_date').all()[:10]
    for sess in PoolSession:
        if sess.event_date >= datetime.date.today()+datetime.timedelta(days=-5):
            sess.deletable = True

    return render(request, 'alldoc/pool_session.html', {"common": common, "PoolSession": PoolSession, "PoolSessionForm": form})


@staff_member_required
def pool_session_delete(request, pk):
    '''Delete Pool session'''
    if request.method == 'POST':
        models.PoolSession.objects.filter(pk=pk).delete()
    return redirect('alldoc_pool_session')


@staff_member_required
def pool_stat(request, start_date=None, end_date=None):
    '''Stat for Pool'''
    common = {"name": "Pool"}

    # Initial-default values
    start_date_init = (timezone.now().date() + timezone.timedelta(days=-365)).replace(day=1)
    end_date_init = timezone.now().date()

    # get form
    form = forms.PoolStatForm(request.GET)
    if form.is_valid():
        common["start_date"] = form.cleaned_data['start_date']
        common["end_date"] = form.cleaned_data['end_date']
    else:
        form = forms.PoolStatForm(initial={"start_date":start_date_init,
                                "end_date":end_date_init})
        common["start_date"] = start_date_init
        common["end_date"] = end_date_init 
    
    # Get data
    PoolSession = models.PoolSession.objects.filter(event_date__gte=common["start_date"]) \
                        .filter(event_date__lte=common["end_date"]).order_by('event_date').all()
    diz = {} # calcolo il group by mese/anno
    list_date = []  
    for sess in PoolSession:
        sess.metri = sess.lap_number * sess.pool.lap_length
        annomese = str(sess.event_date.month).zfill(2)+"-"+str(sess.event_date.year)
        # First month appearence
        if annomese not in list_date:
            diz[annomese] = {'data': sess.event_date.replace(day=1), 
                             'allenamenti': 0, 
                             'vasche (norm)': 0,
                             'metri': 0}
            list_date.append(annomese)
        # Add values
        diz[annomese]['allenamenti'] += 1
        diz[annomese]['vasche (norm)'] += sess.lap_number * 25 / sess.pool.lap_length # normalize to 25m length
        diz[annomese]['metri'] += sess.lap_number * sess.pool.lap_length
    
    # Rechange data
    # diz_final = {'data': [], 'allenamenti': [], 'vasche (norm)': [], 'metri': [], 'vasche media': [], 'metri media': []}
    # for annomese in list_date:
    #     diz_final['data'].append(diz[annomese]['data'])
    #     diz_final['allenamenti'].append(diz[annomese]['allenamenti'])
    #     diz_final['vasche (norm)'].append(diz[annomese]['vasche (norm)'])
    #     diz_final['metri'].append(diz[annomese]['metri'])
    #     diz_final['vasche media'].append(round(diz[annomese]['vasche (norm)']/diz[annomese]['allenamenti'], 2))
    #     diz_final['metri media'].append(round(diz[annomese]['metri']/diz[annomese]['allenamenti'], 2))

    # Highchart
    chart = Highchart(height = 500)
    chart.add_data_set([[1000*(diz[a]['data']-datetime.date(1970,1,1)).total_seconds(), diz[a]['allenamenti']] for a in list_date], 
                        series_type='line', name='Allenamenti')
    chart.add_data_set([[1000*(diz[a]['data']-datetime.date(1970,1,1)).total_seconds(), diz[a]['vasche (norm)']/diz[a]['allenamenti']] for a in list_date], 
                        series_type='bar', name='Media vasche')
    chart.add_data_set([[1000*(diz[a]['data']-datetime.date(1970,1,1)).total_seconds(), diz[a]['metri']/diz[a]['allenamenti']] for a in list_date], 
                        series_type='bar', name='Media metri')
    
    chart.set_options('xAxis', {'type': 'datetime', 'gridLineWidth': 1})
#    chart.set_options('chart', {'backgroundColor':'transparent'})
    chart.set_options('tooltip', {'formatter': 'default_tooltip'})
    chart.set_options('title', {'text': f"Statistiche allenamenti in piscina"})
    chart.htmlcontent;
    chart_dict = {"header": chart.htmlheader, "content":chart.content}

    return render(request, 'alldoc/pool_stat.html', {"common": common, "PoolSession": PoolSession, "form": form, "chart": chart_dict})
