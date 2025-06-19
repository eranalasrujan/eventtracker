from django.contrib import admin
from .models import TimetableSlot, Event, MissedClass

@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = ('faculty','day','start','end')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title','start','end')
    filter_horizontal = ('participants',)

@admin.register(MissedClass)
class MissedClassAdmin(admin.ModelAdmin):
    list_display = ('slot','student','event','timestamp')
    list_filter  = ('slot__day','slot__faculty')
