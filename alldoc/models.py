from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

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
        return f"{self.name} - {self.fuel_type} - {self.description}"


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


    def updateDistance(self):
        '''
        Aggiorna il campo "distance" come differenza tra l'attuale e il precedente
        '''
        supply_prec = Supply.objects.filter(auto=self.auto).filter(distance_total__lt=self.distance_total).order_by('-distance_total').first()
        if supply_prec:
            distance = self.distance_total - supply_prec.distance_total
        else:
            distance = self.distance_total
        Supply.objects.filter(id=self.id).update(distance=distance)
    

    def __str__(self):
        prezzo = round(self.price / self.volume,2)
        return f"{self.event_date} - {self.auto.name} - {self.station} - {self.distance}Km - {prezzo}€/l"


@receiver(post_save, sender=Supply)
def calcDistance(sender, instance, **kwargs):
    '''
    Launch calculation of distance
    '''
    instance.updateDistance()