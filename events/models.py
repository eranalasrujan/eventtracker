# C:\Users\91912\Documents\eventtracker\events\models.py

from django.db import models
from django.conf import settings

class TimetableSlot(models.Model):
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    day     = models.CharField(max_length=3, choices=[
        ('Mon','Monday'),
        ('Tue','Tuesday'),
        ('Wed','Wednesday'),
        ('Thu','Thursday'),
        ('Fri','Friday'),
        ('Sat','Saturday'),
    ])
    start   = models.TimeField()
    end     = models.TimeField()

    def __str__(self):
        return f"{self.faculty.username} {self.day} {self.start}-{self.end}"

class Event(models.Model):
    title        = models.CharField(max_length=200)
    start        = models.DateTimeField()
    end          = models.DateTimeField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.title

class MissedClass(models.Model):
    slot      = models.ForeignKey(TimetableSlot, on_delete=models.CASCADE)
    student   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event     = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('slot','student','event')

    def __str__(self):
        return f"{self.student.username} missed {self.slot}"

# SIGNAL: when participants added, mark missed classes
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=Event.participants.through)
def mark_missed(sender, instance, action, pk_set, **kwargs):
    if action != 'post_add':
        return
    from .models import TimetableSlot, MissedClass
    for uid in pk_set:
        user = instance.participants.model.objects.get(pk=uid)
        if user.role!='student' or not user.batch:
            continue
        day_code   = instance.start.strftime('%a')  # 'Mon', 'Tue', ...
        ev_start   = instance.start.time()
        ev_end     = instance.end.time()
        slots = TimetableSlot.objects.filter(
            faculty__username='sudha',
            day=day_code,
            start__lte=ev_start,
            end__gte=ev_end
        )
        for slot in slots:
            MissedClass.objects.get_or_create(slot=slot, student=user, event=instance)
