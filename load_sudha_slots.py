# load_sudha_slots.py
import os, django
from datetime import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventsystem.settings')
django.setup()

from events.models import TimetableSlot
from django.contrib.auth import get_user_model

User = get_user_model()
faculty = User.objects.get(username='sudhamam')

timetable_data = [
    {'day':'Monday',    'start':'11:15','end':'12:15','subject':'AI','section':'VI-IT'},
    {'day':'Monday',    'start':'14:05','end':'16:05','subject':'OS','section':'IV-IT'},
    {'day':'Tuesday',   'start':'11:15','end':'12:15','subject':'RTP','section':'IV-IT'},
    {'day':'Tuesday',   'start':'13:05','end':'14:05','subject':'AI','section':'VI-IT'},
    {'day':'Wednesday', 'start':'11:15','end':'12:15','subject':'RTP','section':'IV-IT(B2)'},
    {'day':'Wednesday', 'start':'15:05','end':'16:05','subject':'AI','section':'VI-IT'},
    {'day':'Thursday',  'start':'13:05','end':'16:05','subject':'RTP','section':'IV-IT(B1)'},
    {'day':'Saturday',  'start':'09:15','end':'10:15','subject':'DSA','section':'VI-MDP'},
    {'day':'Saturday',  'start':'10:15','end':'11:15','subject':'DSA','section':'VI-MDP'},
    {'day':'Saturday',  'start':'11:15','end':'12:15','subject':'DSA','section':'VI-MDP'},
    {'day':'Saturday',  'start':'16:05','end':'17:05','subject':'DSA','section':'VI-MDP'},
]

for slot in timetable_data:
    sh, sm = map(int, slot['start'].split(':'))
    eh, em = map(int, slot['end'].split(':'))
    TimetableSlot.objects.create(
        faculty=faculty,
        day=slot['day'],
        start=time(sh, sm),
        end=time(eh, em),
        subject=slot['subject'],
        section=slot['section']
    )
print("Re-loaded Sudha’s timetable slots.")
