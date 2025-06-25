from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )
    batch = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="e.g., 'VI-IT', 'VII-CSE'"
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False
    )

    REQUIRED_FIELDS = ['email', 'role']

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username

    def __str__(self):
        return self.username
