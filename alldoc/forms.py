from . import models
from django.forms import Form, ModelForm


class AutoForm(ModelForm):
    class Meta:
        model = models.Auto
        fields = ('name','description','fuel_type')


class StationForm(ModelForm):
    class Meta:
        model = models.Station
        fields = ('name','location')


class SupplyForm(ModelForm):
    class Meta:
        model = models.Supply
        fields = ('event_date','auto','station','volume','price','distance_total')
