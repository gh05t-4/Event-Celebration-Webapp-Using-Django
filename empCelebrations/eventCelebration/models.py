from django.db import models

# Create Table eventClebration_eventslist in empClebrations database
class EventsList(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    event_name = models.CharField(max_length=50)
    event_type = models.CharField(max_length=50)
    event_start_date = models.DateField()
    event_end_date = models.DateField()
    event_img = models.ImageField(upload_to='images/')
    event_description = models.CharField(max_length=280)

# Create Table eventCelebration_presentationevents in empClebrations database
# This table only stores ongoing events and completed events must be deleted
class PresentationEvents(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    presentations_id = models.BigIntegerField(default=0)
    event_name = models.CharField(max_length=50)
    event_type = models.CharField(max_length=50)
    event_end_date = models.DateField()
    event_img = models.CharField(max_length=200)
    event_description = models.CharField(max_length=280)