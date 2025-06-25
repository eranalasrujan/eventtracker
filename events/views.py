from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Event, Notification, TimetableSlot, ProofUpload
from .forms import EventForm, ProofUploadForm, TimetableSlotForm

User = get_user_model()

# --- Role checks ---
def is_student(u): return u.is_authenticated and u.role == 'student'
def is_faculty(u): return u.is_authenticated and u.role == 'faculty'
def is_admin(u):   return u.is_authenticated and u.role == 'admin'

# --- Dashboard router (LOGIN_REDIRECT_URL) ---
@login_required
def dashboard_view(request):
    if request.user.role in ('faculty', 'admin'):
        return redirect('events:faculty_dashboard')
    if request.user.role == 'student':
        return redirect('events:student_dashboard')
    messages.info(request, "No dashboard for your role; showing events list.")
    return redirect('events:event_list')

# --- Event List & Detail ---
@login_required
def event_list(request):
    now = timezone.now()
    upcoming = Event.objects.filter(end_time__gte=now).order_by('start_time')
    past     = Event.objects.filter(end_time__lt=now).order_by('-start_time')
    return render(request, 'events/event_list.html', {
        'upcoming_events': upcoming,
        'past_events':     past,
    })

@login_required
def event_detail(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    is_registered = request.user in ev.attendees.all()
    is_organizer  = (request.user == ev.organizer) or is_admin(request.user)
    attendees     = ev.attendees.order_by('username')
    return render(request, 'events/event_detail.html', {
        'event': ev,
        'is_registered':   is_registered,
        'is_organizer':    is_organizer,
        'registered_attendees': attendees,
    })

# --- Event CRUD ---
@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u), login_url='/accounts/login/')
def event_create(request):
    form = EventForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ev = form.save(commit=False)
        ev.organizer = request.user
        ev.save()
        messages.success(request, f"Created '{ev.title}'.")
        return redirect('events:event_detail', pk=ev.pk)
    return render(request, 'events/event_form.html', {
        'form': form, 'page_title': 'Create Event'
    })

@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u), login_url='/accounts/login/')
def event_edit(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    if not (request.user == ev.organizer or is_admin(request.user)):
        messages.error(request, "Not authorized.")
        return redirect('events:event_detail', pk=pk)
    form = EventForm(request.POST or None, instance=ev)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Updated '{ev.title}'.")
        return redirect('events:event_detail', pk=pk)
    return render(request, 'events/event_form.html', {
        'form': form, 'page_title': f"Edit Event: {ev.title}"}
    )

@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u), login_url='/accounts/login/')
def event_delete(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    if not (request.user == ev.organizer or is_admin(request.user)):
        messages.error(request, "Not authorized.")
        return redirect('events:event_detail', pk=pk)
    if request.method == 'POST':
        title = ev.title
        ev.delete()
        messages.success(request, f"Deleted '{title}'.")
        return redirect('events:event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': ev})

# --- Student Registration & Unregistration ---
@login_required
@user_passes_test(is_student, login_url='/accounts/login/')
def register_event(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    now = timezone.now()
    if ev.end_time < now:
        messages.error(request, "Cannot register past events.")
    elif request.user in ev.attendees.all():
        messages.info(request, "Already registered.")
    else:
        ev.attendees.add(request.user)
        Notification.objects.create(
            user=request.user,
            event=ev,
            message=f"You registered for '{ev.title}'."
        )
        messages.success(request, f"Registered for '{ev.title}'.")
    return redirect('events:event_detail', pk=pk)

@login_required
@user_passes_test(is_student, login_url='/accounts/login/')
def unregister_event(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    if request.user in ev.attendees.all():
        ev.attendees.remove(request.user)
        Notification.objects.create(
            user=request.user,
            event=ev,
            message=f"You unregistered from '{ev.title}'."
        )
        messages.success(request, f"Unregistered from '{ev.title}'.")
    else:
        messages.info(request, "You were not registered.")
    return redirect('events:event_detail', pk=pk)

# --- Guest Roll Numbers (Faculty/Admin) ---
@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u), login_url='/accounts/login/')
def add_guest_participants(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        ev.guest_numbers = request.POST.get('guest_numbers', '')
        ev.save()
        messages.success(request, "Updated guest participants.")
    return redirect('events:event_detail', pk=pk)

# --- Proof Upload ---
@login_required
@user_passes_test(is_student, login_url='/accounts/login/')
def proof_upload(request):
    form = ProofUploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        proof = form.save(commit=False)
        if proof.attendee != request.user:
            messages.error(request, "You can only upload for yourself.")
            return render(request, 'events/proof_upload.html', {'form': form})
        proof.save()
        Notification.objects.create(
            user=request.user,
            event=proof.event,
            message=f"Proof uploaded for '{proof.event.title}'."
        )
        messages.success(request, "Proof uploaded.")
        return redirect('events:event_list')
    form.fields['attendee'].queryset = User.objects.filter(pk=request.user.pk)
    form.fields['event'].queryset    = Event.objects.filter(attendees=request.user)
    return render(request, 'events/proof_upload.html', {'form': form})

# --- Notifications List ---
@login_required
def notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    for n in notes:
        if not n.is_read:
            n.is_read = True
            n.save()
    return render(request, 'events/notifications.html', {'notifications': notes})

# --- Student Dashboard (Upcoming / Past) ---
@login_required
@user_passes_test(is_student, login_url='/accounts/login/')
def student_dashboard(request):
    now = timezone.now()
    upcoming = request.user.attended_events.filter(end_time__gte=now).order_by('start_time')
    past     = request.user.attended_events.filter(end_time__lt=now).order_by('-start_time')
    organized= request.user.organized_events.all().order_by('-start_time')
    return render(request, 'events/student_dashboard.html', {
        'my_upcoming_events': upcoming,
        'my_past_events':     past,
        'my_organized_events':organized,
    })

# --- Faculty Dashboard (7 days × 6 periods) ---
# events/views.py

from django.shortcuts           import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils               import timezone
from datetime                   import datetime, timedelta
from django.contrib.auth        import get_user_model

from .models import TimetableSlot, Event

CustomUser = get_user_model()

def is_faculty(user):
    return user.is_authenticated and user.role in ('faculty', 'admin')

@login_required
@user_passes_test(is_faculty, login_url='accounts:login')
def faculty_dashboard(request, day=None):
    # 1️⃣ Determine the date to display
    today = timezone.localdate()
    if day:
        try:
            selected = datetime.strptime(day, '%Y-%m-%d').date()
        except ValueError:
            selected = today
    else:
        selected = today

    selected_day = selected.strftime('%A')  # e.g. "Monday"

    # 2️⃣ Fetch all TimetableSlot for this faculty on that weekday
    slots = TimetableSlot.objects.filter(
        faculty=request.user,
        day=selected_day
    ).order_by('start')

    # 3️⃣ Fetch all events happening on that selected date
    events_on_date = Event.objects.filter(start_time__date=selected)

    # 4️⃣ Build slot_misses
    slot_misses = []
    for slot in slots:
        # Combine date + slot times into aware datetimes
        start_dt = timezone.make_aware(datetime.combine(selected, slot.start))
        end_dt   = timezone.make_aware(datetime.combine(selected, slot.end))

        # Find events overlapping this slot window
        overlapping = events_on_date.filter(
            start_time__lt=end_dt,
            end_time__gt=start_dt
        )

        # From those events, pick only student-attendees whose batch == slot.section
        missed_usernames = overlapping.filter(
            attendees__role='student',
            attendees__batch=slot.section
        ).values_list('attendees__username', flat=True).distinct()

        slot_misses.append({
            'slot':     slot,
            'students': sorted(missed_usernames),
        })

    # 5️⃣ Build date navigation (±3 days)
    nav_dates = []
    for offset in range(-3, 4):
        dt = selected + timedelta(days=offset)
        nav_dates.append({
            'label':    dt.strftime('%a %d'),
            'url':      dt.strftime('%Y-%m-%d'),
            'selected': (dt == selected),
        })

    # 6️⃣ Render, passing slot_misses (not dashboard_data)
    return render(request, 'events/faculty_dashboard.html', {
        'slot_misses':  slot_misses,
        'nav_dates':    nav_dates,
        'selected_day': selected_day,
    })


# --- Add/Delete Timetable Slot ---
@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u), login_url='/accounts/login/')
def add_timetable_slot(request):
    if request.method == 'POST':
        form = TimetableSlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.faculty = request.user
            slot.save()
            messages.success(request, "Timetable slot added.")
        else:
            messages.error(request, "Error adding slot.")
    return redirect('events:faculty_dashboard')

@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u), login_url='/accounts/login/')
def delete_timetable_slot(request, pk):
    slot = get_object_or_404(TimetableSlot, pk=pk)
    if slot.faculty == request.user or is_admin(request.user):
        slot.delete()
        messages.success(request, "Slot deleted.")
    else:
        messages.error(request, "Not authorized.")
    return redirect('events:faculty_dashboard')
