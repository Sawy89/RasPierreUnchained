from . import models
from django.forms import Form, ModelForm, DateTimeField
from django.forms.widgets import DateTimeInput
from django.utils import timezone


class AutoForm(ModelForm):
    class Meta:
        model = models.Auto
        fields = ('name','description','fuel_type')


class StationForm(ModelForm):
    class Meta:
        model = models.Station
        fields = ('name','location')


class SupplyForm(ModelForm):

    event_date = DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        initial=timezone.now().date(),
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = models.Supply
        fields = ('event_date','auto','station','volume','price','distance_total')
