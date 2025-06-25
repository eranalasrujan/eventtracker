from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from datetime import datetime, time # Import time for TimetableSlot

# 1. Event model
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField() # Timezone-aware datetime
    end_time = models.DateTimeField()   # Timezone-aware datetime
    location = models.CharField(max_length=200)
    
    # Organizer of the event (ForeignKey to CustomUser)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='organized_events')
    
    # Many-to-many to users (students/faculty) attending the event
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attended_events', blank=True) # Changed related_name
    
    max_attendees = models.PositiveIntegerField(null=True, blank=True, help_text="Leave blank for unlimited attendees.")
    
    # For external events, students might create them and require proof
    is_external = models.BooleanField(default=False, help_text="Check if this is an external event (student-created).")
    requires_proof = models.BooleanField(default=False, help_text="Check if proof upload is required for this event.")
    
    # For guest participants (non-registered users), e.g., roll numbers entered manually
    guest_numbers = models.TextField(blank=True, help_text="Comma-separated roll numbers of guest participants.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.start_time.date()})"

    # Helper properties for templates and views
    @property
    def is_past(self):
        return self.end_time < timezone.now()

    @property
    def is_full(self):
        if self.max_attendees is None:
            return False
        return self.attendees.count() >= self.max_attendees

    @property
    def total_attendees_count(self):
        registered_count = self.attendees.count()
        guest_count = len(self.guest_numbers_list)
        return registered_count + guest_count
    
    @property
    def guest_numbers_list(self):
        if self.guest_numbers:
            return [roll.strip() for roll in self.guest_numbers.split(',') if roll.strip()]
        return # Return empty list if no guest numbers


# 2. Notification model
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications') # Changed field name to 'user'
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True) # Optional link to an event
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.message}" # Updated to use self.user.username

    class Meta:
        ordering = ['-created_at']


# 3. TimetableSlot model (Re-integrated as per user's provided snippet)
class TimetableSlot(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='timetable_slots')
    day = models.CharField(max_length=9, choices=DAY_CHOICES) # Increased max_length for full day names
    start_time = models.TimeField() # Changed from 'start' to 'start_time' for clarity
    end_time = models.TimeField()   # Changed from 'end' to 'end_time' for clarity
    topic = models.CharField(max_length=255, blank=True, null=True) # Changed from 'topic' to 'topic' for clarity

    class Meta:
        unique_together = ('faculty', 'day', 'start_time', 'end_time') # Updated field names in unique_together
        ordering = ['day', 'start_time'] # Order for display

    def __str__(self):
        return f"{self.faculty.username}'s {self.day} slot ({self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')})"
    
    @property
    def duration(self):
        # Combine with a dummy date to calculate duration
        dt_start = datetime.combine(timezone.localdate(), self.start_time)
        dt_end = datetime.combine(timezone.localdate(), self.end_time)
        return (dt_end - dt_start).total_seconds() / 60


# 4. ProofUpload model
def proof_upload_path(instance, filename):
    # Files will be saved to MEDIA_ROOT/proofs/<username>/<event_title_slug>/<filename>
    username = 'unknown_user'
    event_title_slug = 'unknown_event'
    if instance.attendee: # ProofUpload links directly to Attendee (CustomUser)
        username = instance.attendee.username
    if instance.event: # Assuming ProofUpload links directly to Event
        event_title_slug = slugify(instance.event.title)
    
    return f'proofs/{username}/{event_title_slug}/{filename}'

class ProofUpload(models.Model):
    # This model is specifically for proof of attendance for an event
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='proofs')
    attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proofs_uploaded')
    file = models.FileField(upload_to=proof_upload_path) # File will be saved to MEDIA_ROOT/proofs/...
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, help_text="Optional description for the proof.")

    def __str__(self):
        return f"Proof for {self.attendee.username} for {self.event.title}"
    


# events/models.py

from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class TimetableSlot(models.Model):
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    day     = models.CharField(max_length=10)    # e.g. "Monday"
    start   = models.TimeField()                 # <— named “start”
    end     = models.TimeField()                 # <— named “end”
    subject = models.CharField(max_length=100)
    section = models.CharField(max_length=50)     # e.g. "VI-IT"

    def __str__(self):
        return f"{self.day} {self.start}-{self.end} ({self.subject})"
