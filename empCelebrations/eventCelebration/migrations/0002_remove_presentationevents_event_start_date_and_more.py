# Generated by Django 4.2.4 on 2023-08-10 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventCelebration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presentationevents',
            name='event_start_date',
        ),
        migrations.AlterField(
            model_name='presentationevents',
            name='event_img',
            field=models.CharField(max_length=200),
        ),
    ]
