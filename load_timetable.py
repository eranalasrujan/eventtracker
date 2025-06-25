# load_timetable.py
import os
import django
from datetime import datetime

# 1. Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventsystem.settings')
django.setup()

# 2. Imports
from django.contrib.auth import get_user_model
from events.models import TimetableSlot

User = get_user_model()

# 3. Get Sudha’s user
try:
    sudha = User.objects.get(username='sudhamam')
except User.DoesNotExist:
    print("👩‍🏫  User 'sudhamam' not found—did you run createsuperuser and create that faculty account?")
    exit(1)

# 4. Define her weekly slots
timetable_data = [
    # Monday
    {'day':'Monday',    'start':'11:15','end':'12:15','subject':'AI', 'section':'VI-IT'},
    {'day':'Monday',    'start':'14:05','end':'16:05','subject':'OS', 'section':'IV-IT'},

    # Tuesday
    {'day':'Tuesday',   'start':'11:15','end':'12:15','subject':'RTP','section':'IV-IT'},
    {'day':'Tuesday',   'start':'13:05','end':'14:05','subject':'AI', 'section':'VI-IT'},

    # Wednesday
    {'day':'Wednesday', 'start':'11:15','end':'12:15','subject':'RTP','section':'IV-IT(B2)'},
    {'day':'Wednesday', 'start':'15:05','end':'16:05','subject':'AI', 'section':'VI-IT'},

    # Thursday
    {'day':'Thursday',  'start':'13:05','end':'16:05','subject':'RTP','section':'IV-IT(B1)'},

    # Saturday
    {'day':'Saturday',  'start':'09:15','end':'10:15','subject':'DSA','section':'VI-MDP'},
    {'day':'Saturday',  'start':'10:15','end':'11:15','subject':'DSA','section':'VI-MDP'},
    {'day':'Saturday',  'start':'11:15','end':'12:15','subject':'DSA','section':'VI-MDP'},
    {'day':'Saturday',  'start':'16:05','end':'17:05','subject':'DSA','section':'VI-MDP'},
]

# 5. Create slots
for entry in timetable_data:
    start_time = datetime.strptime(entry['start'], '%H:%M').time()
    end_time   = datetime.strptime(entry['end'],   '%H:%M').time()

    slot, created = TimetableSlot.objects.get_or_create(
        faculty = sudha,
        day     = entry['day'],
        start   = start_time,
        end     = end_time,
        section = entry['section'],
        defaults={'subject': entry['subject']}
    )
    if created:
        print(f"✅ Created: {entry['day']} {entry['start']}-{entry['end']} ({entry['section']})")
    else:
        print(f"✏️ Exists:  {entry['day']} {entry['start']}-{entry['end']} ({entry['section']})")

print("All done! 🎉")
