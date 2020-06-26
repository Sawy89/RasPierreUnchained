from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

# Create your models here.
class Auto(models.Model):
    '''
    Class for Automobile
    '''
    db_table = 'fuel_auto'
    
    class FuelType(models.TextChoices):
        '''
        FuelType available
        https://stackoverflow.com/questions/54802616/how-to-use-enums-as-a-choice-field-in-django-model
        https://docs.djangoproject.com/en/dev/ref/models/fields/#field-choices-enum-types
        '''
        DIESEL = 'Diesel'
        BENZINA = 'Benzina'
        ELETTRICA = 'Elettrica'

    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=1024, default=None, blank=True, null=True)
    fuel_type = models.CharField(max_length=10, choices=FuelType.choices)
    insertdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        str_r = f"{self.name} [{self.fuel_type}]"
        return str_r


class Station(models.Model):
    '''
    Class for gas Station = distributori
    '''
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    insertdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'location',)

    def __str__(self):
        return f"{self.name} [{self.location}]"


class Supply(models.Model):
    '''
    Classe per i rifornimenti
    '''
    db_table = 'fuel_supply'

    event_date = models.DateField()
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name="supply")
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="supply")
    volume = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    distance_total = models.IntegerField()
    distance = models.IntegerField(default=None, blank=True, null=True)
    insertdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event_date', 'auto',)


    def save(self, *args, **kwargs):
        supply_pre = Supply.objects.filter(auto=self.auto).filter(event_date__lt=self.event_date).order_by('-event_date').first()
        if not(supply_pre) or supply_pre.distance_total < self.distance_total:
            super(Supply, self).save(*args, **kwargs)
        else:
            raise ValidationError('La distanza deve aumentare')


    def updateDistance(self):
        '''
        Aggiorna il campo "distance" come differenza tra l'attuale e il precedente
        '''
        supply_pre = Supply.objects.filter(auto=self.auto).filter(distance_total__lt=self.distance_total).order_by('-distance_total').first()
        if supply_pre:
            distance = self.distance_total - supply_pre.distance_total
        else:
            distance = self.distance_total
        Supply.objects.filter(id=self.id).update(distance=distance)
    

    def __str__(self):
        prezzo = round(self.price / self.volume,2)
        return f"{self.event_date} - {self.auto.name} - {self.distance_total}km - {self.station} - {self.volume}/{self.distance}={round(self.distance/self.volume,2)}km/l - {prezzo}€/litro"
    
    
    def _calcPrice(self):
        self.pricevolume = round(self.price / self.volume, 2)
        self.pricedistance = round(self.price / self.distance, 2)
    
    def _calcConsumption(self):
        self.consumption1 = round(self.distance / self.volume, 2)
        self.consumption2 = round(self.volume * 100 / self.distance, 2)


    def calcStat(self):
        '''Calculate Statistics'''
        self._calcPrice()
        self._calcConsumption()



@receiver(post_save, sender=Supply)
def calcDistance(sender, instance, **kwargs):
    '''
    Launch calculation of distance
    '''
    # Update current
    instance.updateDistance()
    # Update all followinf (if any)
    supply_list = Supply.objects.filter(auto=instance.auto).filter(distance_total__gt=instance.distance_total).all() 
    for supply in supply_list:
        supply.updateDistance()