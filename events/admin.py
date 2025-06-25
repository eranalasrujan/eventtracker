# events/admin.py

from django.contrib import admin
from .models import Event, Notification, TimetableSlot, ProofUpload

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'location',
        'start_time',
        'end_time',
        'organizer',
        'is_external',
        'requires_proof',
        'created_at',
    )
    list_filter = (
        'is_external',
        'requires_proof',
        'start_time',
        'end_time',
        'organizer__role',
    )
    search_fields = (
        'title',
        'description',
        'location',
        'organizer__username',
    )
    raw_id_fields = (
        'organizer',
        'attendees',
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'event',
        'message',
        'is_read',
        'created_at',
    )
    list_filter = (
        'is_read',
        'created_at',
        'user',
        'event',
    )
    search_fields = (
        'message',
        'user__username',
        'event__title',
    )
    raw_id_fields = (
        'user',
        'event',
    )

@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = (
        'faculty',   # FK to your CustomUser
        'day',       # e.g. "Monday"
        'start',     # TimeField
        'end',       # TimeField
        'subject',   # CharField for topic/subject
    )
    list_filter = (
        'faculty',
        'day',
    )
    search_fields = (
        'faculty__username',
        'subject',
    )
    raw_id_fields = (
        'faculty',
    )

@admin.register(ProofUpload)
class ProofUploadAdmin(admin.ModelAdmin):
    list_display = (
        'event',
        'attendee',
        'file',
        'uploaded_at',
        'description',
    )
    list_filter = (
        'uploaded_at',
        'event',
        'attendee',
    )
    search_fields = (
        'event__title',
        'attendee__username',
        'description',
    )
    raw_id_fields = (
        'event',
        'attendee',
    )
