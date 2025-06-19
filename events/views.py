# C:\Users\91912\Documents\eventtracker\events\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TimetableSlot, MissedClass, Event
from .forms import EventForm

def event_list(request):
    events = Event.objects.all().order_by('start')
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def sudha_dashboard(request):
    if request.user.username!='sudha':
        return redirect('event_list')
    days = ['Mon','Tue','Wed','Thu','Fri','Sat']
    grid = []
    for d in days:
        slots = TimetableSlot.objects.filter(faculty=request.user, day=d).order_by('start')
        row = []
        for s in slots:
            missed = MissedClass.objects.filter(slot=s).values_list('student__username', flat=True)
            row.append({
                'slot': f"{s.start.strftime('%H:%M')}–{s.end.strftime('%H:%M')}",
                'missed': list(missed)
            })
        grid.append({'day': d, 'slots': row})
    return render(request, 'events/sudha_dashboard.html', {'grid': grid})

@login_required
def event_create(request):
    if request.user.role not in ['admin','faculty']:
        return redirect('event_list')
    if request.method=='POST':
        form = EventForm(request.POST)
        if form.is_valid():
            ev = form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})
