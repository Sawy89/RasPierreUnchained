from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from apscheduler.schedulers.background import BackgroundScheduler
from . import xmasg


class Room(models.Model):
    '''
    Class for Room = Stanza
    '''
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()       # final date (for countdown)
    member = models.ManyToManyField(User, through='RoomMember', related_name="rooms")
    job_id = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.name}"


@receiver(pre_save, sender=Room)
def setRoomEndDate(sender, instance, **kwargs):
    '''
    Set the timeout of the room for the extraction!
    '''
    # ToDO: save job ID on DB
    # ToDo: reload all event on startup!
    # Add the job to the scheduler
    scheduler = BackgroundScheduler()
    print(f"Event will start at {instance.end_date}")
    job = scheduler.add_job(xmasg.stampa, 'date', run_date=instance.end_date, args=[instance.name])     # https://apscheduler.readthedocs.io/en/stable/modules/triggers/date.html#module-apscheduler.triggers.date
    scheduler.start()

    # Save job id on DB
    instance.job_id = job.id


class RoomMessage(models.Model):
    '''
    Class for all messages exchanged
    '''
    message = models.CharField(max_length=5000)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="message")
    insert_date = models.DateTimeField(auto_now_add=True)


class RoomMember(models.Model):
    '''
    Class for exclusion (people not to be extracted for that person)
    '''
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="members")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="room_members")
    is_admin = models.BooleanField(default=False)
    exclusion = models.ManyToManyField(User, blank=True, related_name="room_exclusions")

    def has_as_exclusion(self, user_to_check):
        if user_to_check in self.exclusion.all():
            return True
        else:
           return False


class XmasGift(models.Model):
    '''
    Class for extraction of the sender and receiver
    '''
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="extraction")
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="extractions_giver")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="extractions_receiver")
