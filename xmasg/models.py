from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
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
    member = models.ManyToManyField(User, through='RoomMember', through_fields=('room', 'member'), related_name="rooms")
    job_id = models.CharField(max_length=128, blank=True)
    extraction_done = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        return f"{self.name}"


@receiver(post_save, sender=Room)
def setRoomEndDate(sender, instance, **kwargs):
    '''
    Set the timeout of the room for the extraction!
    '''
    # ToDo: reload all event on startup!
    # ToDO: check that the date of the job scheduler is the same
    # Add the job to the scheduler (only if not present)
    scheduler = BackgroundScheduler()
    if instance.job_id not in [i.id for i in scheduler.get_jobs()]:
        print(f"Event for room {instance} will start at {instance.end_date}")
        job = scheduler.add_job(xmasg.xmasg_extraction, 'date', run_date=instance.end_date, args=[instance.id])     # https://apscheduler.readthedocs.io/en/stable/modules/triggers/date.html#module-apscheduler.triggers.date
        scheduler.start()

        # Update on DB
        Room.objects.filter(pk=instance.id).update(job_id=job.id) # update should not launch this function again


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
    # ToDo: only add member and accept modification if enddate is available
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="members")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="room_members")
    is_admin = models.BooleanField(default=False)
    exclusion = models.ManyToManyField(User, blank=True, related_name="room_exclusions")
    receiver = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE, related_name="receiver")

    def has_as_exclusion(self, user_to_check):
        if user_to_check in self.exclusion.all():
            return True
        else:
           return False

