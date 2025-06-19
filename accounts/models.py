# C:\Users\91912\Documents\eventtracker\accounts\models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin',   'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    ]
    role  = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    batch = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
