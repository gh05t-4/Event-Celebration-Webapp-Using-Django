from django import forms
from .models import EventsList

EVENT_TYPES = [
    ('bday', "Employee Birthday"),
    ('empMonth', "Employee of the month"),
    ('festival', "Festival"),
    ('promotion', "Promotion"),
]

class AddNewEventList(forms.Form):
    event_name = forms.CharField(label="Event Name", max_length=50)
    event_type = forms.CharField(label="Event Type", widget=forms.Select(choices=EVENT_TYPES))
    event_start_date = forms.CharField(label="Event Start Date", widget=forms.DateInput(attrs={'type': 'date'}))
    event_end_date = forms.CharField(label="Event End Date", widget=forms.DateInput(attrs={'type': 'date'}))
    event_img = forms.ImageField(label="Event Image")
    event_description = forms.CharField(label="Event Description", max_length=280, widget=forms.Textarea)

# To perform update operation use this form 
class EditedEventsList(forms.ModelForm):
    class Meta:
        model = EventsList
        fields = '__all__'