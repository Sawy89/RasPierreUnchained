from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
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
    gift_date = models.DateTimeField()      # Date of the physical gift exchange
    member = models.ManyToManyField(User, through='RoomMember', through_fields=('room', 'member'), related_name="rooms")
    job_id = models.CharField(max_length=128, blank=True)
    extraction_done = models.CharField(max_length=1024, blank=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
    
    def getNumberAdmin(self):
        '''Get the number of admin'''
        n_admin = 0
        for u in RoomMember.objects.filter(room=self).all():
            if u.is_admin == True:
                n_admin += 1    # count number of admin
        return n_admin

@receiver(post_save, sender=Room)
def setRoomEndDate(sender, instance, **kwargs):
    '''
    Set the timeout of the room for the extraction!
    '''
    # ToDo: reload all event on startup!
    # ToDO: check that the date of the job scheduler is the same
    # Add the job to the scheduler (only if not present)
    scheduler = BackgroundScheduler()
    if instance.job_id not in [i.id for i in scheduler.get_jobs()]  and  instance.end_date < timezone.now():
        print(f"Event for room {instance} will start at {instance.end_date}")
        job = scheduler.add_job(xmasg.xmasg_extraction, 'date', run_date=instance.end_date, args=[instance.id])     # https://apscheduler.readthedocs.io/en/stable/modules/triggers/date.html#module-apscheduler.triggers.date
        scheduler.start()

        # Update on DB
        Room.objects.filter(pk=instance.id).update(job_id=job.id) # update should not launch this function again


class RoomMember(models.Model):
    '''
    Class for exclusion (people not to be extracted for that person)
    '''
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

