import os
from datetime import date
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict

from .models import EventsList, PresentationEvents
from .forms import AddNewEventList, EditedEventsList

@login_required
def index(request):
    """Admin Dashboard Page to Read the data from the database and
       adds ongoing events to presentation table"""

    if request.method == "GET":
        # Display the details of events stored in the database
        # Provide option for CRUD operations.
        model = EventsList.objects.all()
        
        return render(request, "eventCelebration/index.html", {'model': model})

@login_required
def addEvent(request):
    """Create a new event and adds it to the database"""

    if request.method == "GET":
        # Display the form to add a new event
        form = AddNewEventList()

        return render(request, "eventCelebration/addEvent.html", {'form': form})
    elif request.method == "POST":
        # Store the new event to the database
        form = AddNewEventList(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data['event_name'])
            model = EventsList(event_name=form.cleaned_data['event_name'], event_type=form.cleaned_data['event_type'], event_start_date=form.cleaned_data['event_start_date'], event_end_date=form.cleaned_data['event_end_date'], event_img=form.cleaned_data['event_img'], event_description=form.cleaned_data['event_description'])
            model.save()
            messages.success(request, 'Event was successfully added.')
            return redirect('../')
        else:
            return render(request, "eventCelebration/addEvent.html", {'form': form, 'errorMsg': "Invalid Form"})

@login_required
def editEvent(request, pk):
    """Update the event stored in the database"""

    if request.method == "GET":
        event_details = get_object_or_404(EventsList, pk=pk)

        # Change the type object to python dictionary
        event_details_dict = model_to_dict(event_details)
        
        # Fill the form with the values in the database
        form = AddNewEventList(initial=event_details_dict)

        return render(request, 'eventCelebration/editEvent.html', {'form': form, 'pk': pk})
    elif request.method == "POST":
        event_details = get_object_or_404(EventsList, pk=pk)

        # Get old image path to remove it if the event_img is updated
        old_image_path = event_details.event_img.path

        form = EditedEventsList(request.POST or None, request.FILES or None, instance=event_details)

        if form.is_valid():
            # commit=False returns an object that hasn't yet been saved to the database
            event_details = form.save(commit=False)

            if 'event_img' in form.cleaned_data:
                event_details.event_img = form.cleaned_data['event_img']

            event_details.save()

            # if the data is changed in EventsList model then update the 
            # PresentationEvents model if that instance exists
            if PresentationEvents.objects.filter(presentations_id=pk).exists():
                presentation_instance = PresentationEvents.objects.get(presentations_id=pk)

                presentation_instance.event_name = event_details.event_name
                presentation_instance.event_type = event_details.event_type
                presentation_instance.event_end_date = event_details.event_end_date
                presentation_instance.event_img = event_details.event_img.url
                presentation_instance.event_description = event_details.event_description

                presentation_instance.save()

            # remove old image
            if old_image_path != event_details.event_img.path:
                os.remove(old_image_path)

            messages.success(request, 'Event was successfully changed.')

            return redirect('../../')

        messages.error(request, 'Something went wrong')
        return redirect('../../')

@login_required
def deleteEvent(request, pk):
    """Delete the event stored in the database"""

    if request.method == "POST":

        try:
            event_to_delete = get_object_or_404(EventsList, pk=pk)
            os.remove(event_to_delete.event_img.path)
            event_to_delete.delete()
            messages.success(request, 'Event was successfully deleted.')
            return redirect('../../')

        except:
            messages.error(request, 'Event does not exist.')
            return redirect('../../')

def presentEvents(request):
    """Displays ongoing events and removes the finished events from the presentation table"""

    if request.method == "GET":
        # Get the data from the eventCelebration_presentationevents table to check
        # if any event is to deleted
        model = PresentationEvents.objects.all()

        # Delete the events that have exceeded event_end_date
        for row in model:
            if row.event_end_date < date.today():
                row.delete()

        # Add events to PresentationEvents model if the events have started
        model = EventsList.objects.all()

        for row in model:
            # Check if the event has started and only add it to PresentationEvents model if it
            # does'nt already exists
            if row.event_start_date <= date.today() and row.event_end_date >= date.today() and not PresentationEvents.objects.filter(presentations_id=row.event_id).exists():
                presentation_instance = PresentationEvents()

                presentation_instance.presentations_id = row.event_id
                presentation_instance.event_name = row.event_name
                presentation_instance.event_type = row.event_type
                presentation_instance.event_end_date = row.event_end_date
                presentation_instance.event_img = row.event_img.url
                presentation_instance.event_description = row.event_description

                presentation_instance.save()

        # Get the updated data from the eventCelebration_presentationevents
        # if any data is deleted
        model = PresentationEvents.objects.all()

        events = []
        for row in model:
            events.append(
                {
                    'eventName': row.event_name,
                    'eventType': row.event_type,
                    'eventImg': row.event_img,
                    'eventDescription': row.event_description,
                }
            )

        return render(request, "eventCelebration/presentEvents.html", {'events': json.dumps(events)})
