import os
import django

# Set the settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventsystem.settings')
# adjust if your project is named differently
django.setup()

from django.contrib.auth import get_user_model
from django.utils.text import slugify

FACULTY_FILE = os.path.join(os.getcwd(), 'faculty.txt')
User = get_user_model()

with open(FACULTY_FILE, encoding='utf-8') as f:
    for line in f:
        full_name = line.strip()
        if not full_name:
            continue
        username = slugify(full_name).replace('-', '_')
        if User.objects.filter(username=username).exists():
            print(f"Skipping existing user: {username}")
            continue
        user = User.objects.create_user(
            username=username,
            password=username
        )
        user.role = 'faculty'
        user.save()
        print(f"Created faculty user: {username}")
