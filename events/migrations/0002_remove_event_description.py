# Generated by Django 5.2.2 on 2025-06-05 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='description',
        ),
    ]
