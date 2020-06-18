from . import models
from django.forms import Form, ModelForm, DateTimeField
from django.forms.widgets import DateTimeInput
from django.utils import timezone
from django.core.exceptions import ValidationError


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

        
    def clean(self):
        '''
        Add checks before saving:
        - the distance increase in time
        - the date is not the same as another one
        '''
        super().clean()
        # Check distance increate
        supply_pre = models.Supply.objects.filter(auto=self.cleaned_data.get('auto')).filter(event_date__lt=self.cleaned_data.get('event_date')).order_by('-event_date').first()
        if supply_pre and supply_pre.distance_total >= self.cleaned_data.get('distance_total'):
            self.add_error('distance_total', 'La distanza deve aumentare')
            raise ValidationError('La distanza deve aumentare')
        # Check event_date is unique
        supply_pre = models.Supply.objects.filter(auto=self.cleaned_data.get('auto')).filter(event_date=self.cleaned_data.get('event_date')).first()
        if supply_pre:
            self.add_error('event_date', 'Data già inserita')
            raise ValidationError('Data già inserita')

    class Meta:
        model = models.Supply
        fields = ('event_date','auto','station','volume','price','distance_total')

            
