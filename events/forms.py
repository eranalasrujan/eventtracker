from django import forms
from.models import Event, ProofUpload, TimetableSlot
from django.contrib.auth import get_user_model
from django.forms.widgets import DateInput, TimeInput # For HTML5 date/time inputs

CustomUser = get_user_model()

# Form for creating/editing events
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'location', 'max_attendees', 'is_external', 'requires_proof', 'guest_numbers']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), # HTML5 datetime-local
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), # HTML5 datetime-local
        }
    
    # Custom validation for start_time and end_time
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")
        
        return cleaned_data

# Form for uploading proof files
class ProofUploadForm(forms.ModelForm):
    class Meta:
        model = ProofUpload
        fields = ['event', 'attendee', 'file', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the event and attendee dropdowns to be more descriptive
        self.fields['event'].queryset = Event.objects.all().order_by('title')
        self.fields['event'].label_from_instance = lambda obj: f"{obj.title} ({obj.start_time.strftime('%Y-%m-%d %H:%M')})"
        
        self.fields['attendee'].queryset = CustomUser.objects.all().order_by('username')
        self.fields['attendee'].label_from_instance = lambda obj: f"{obj.username} ({obj.get_full_name() or obj.role})"

# Form for creating Timetable Slots
from django import forms
from .models import TimetableSlot

class TimetableSlotForm(forms.ModelForm):
    class Meta:
        model = TimetableSlot
        fields = [
            'faculty',
            'day',
            'start',
            'end',
            'subject',
            'section',
        ]
        widgets = {
            'start': forms.TimeInput(attrs={'type': 'time'}),
            'end': forms.TimeInput(attrs={'type': 'time'}),
        }

    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")
        
        return cleaned_data