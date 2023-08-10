from django.contrib import admin
from .models import EventsList, PresentationEvents

# Register your models here.
admin.site.register(EventsList)
admin.site.register(PresentationEvents)
