# events/urls.py

from django.urls import path
from .views import (
    dashboard_view,
    event_list,
    event_detail,
    event_create,
    event_edit,
    event_delete,
    register_event,
    unregister_event,
    add_guest_participants,
    notifications,
    proof_upload,
    student_dashboard,
    faculty_dashboard,
    add_timetable_slot,
    delete_timetable_slot,
)

app_name = 'events'

urlpatterns = [
    # Root URL → dashboard by role
    path('', dashboard_view, name='dashboard'),

    # Event listing & detail
    path('events/',              event_list,   name='event_list'),
    path('events/<int:pk>/',     event_detail, name='event_detail'),

    # Event CRUD (faculty/admin only)
    path('events/create/',       event_create, name='event_create'),
    path('events/<int:pk>/edit/',   event_edit,   name='event_edit'),
    path('events/<int:pk>/delete/', event_delete, name='event_delete'),

    # Student registration & guest-management
    path('events/<int:pk>/register/',   register_event,        name='register_event'),
    path('events/<int:pk>/unregister/', unregister_event,      name='unregister_event'),
    path('events/<int:pk>/add_guests/', add_guest_participants, name='add_guest_participants'),

    # Notifications
    path('notifications/',       notifications, name='notifications'),

    # Proof uploads
    path('proof_upload/',        proof_upload,  name='proof_upload'),

    # Dashboards
    path('student/dashboard/',   student_dashboard, name='student_dashboard'),
    path('faculty/dashboard/',   faculty_dashboard, name='faculty_dashboard'),
    path('faculty/dashboard/<slug:day>/', faculty_dashboard, name='faculty_dashboard_day'),

    # Timetable-slot management (faculty/admin only)
    path('faculty/slots/add/',          add_timetable_slot,   name='add_timetable_slot'),
    path('faculty/slots/<int:pk>/delete/', delete_timetable_slot, name='delete_timetable_slot'),
]
