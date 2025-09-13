from django.shortcuts import render, redirect, get_object_or_404
from events.forms import EventForm
from events.models import Event, Participant
from django.utils import timezone
from django.db.models import Q
import datetime
from django.contrib import messages


# Home Page with Search
def home(request):
    query = request.GET.get("q") 
    if query:
        events = Event.objects.filter(
            Q(name__icontains=query) | Q(date__icontains=query) | Q(location__icontains=query)
        )
    else:
        events = Event.objects.all()

    return render(request, "home.html", {
        "events": events,
        "query": query
    })


# Dashboard with Filters (today / total / upcoming / past)
def dashboard(request):
    today = timezone.localdate()

    # Default filter = today
    filter_type = request.GET.get("filter", "today")

    if filter_type == "total":
        events = Event.objects.all()
        section_title = "All Events"
    elif filter_type == "upcoming":
        events = Event.objects.filter(date__gt=today)
        section_title = "Upcoming Events"
    elif filter_type == "past":
        events = Event.objects.filter(date__lt=today)
        section_title = "Past Events"
    else:
        events = Event.objects.filter(date=today)
        section_title = "Today's Events"

    context = {
        "total_event": Event.objects.count(),
        "upcomming_events": Event.objects.filter(date__gt=today).count(),
        "past_events": Event.objects.filter(date__lt=today).count(),
        "total_participants": Participant.objects.count(),
        "todays_events": events,
        "section_title": section_title,
    }
    return render(request, "dashboard.html", context)


# Create Event
def create_event(request):
    form = EventForm()

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "event_form.html", {
                "form": EventForm(),  
                "message": "✅ Event Added Successfully!"
            })

    context = {"form": form}
    return render(request, "event_form.html", context)


def update_event(request,id):
    event = Event.objects.get(id=id)
    form = EventForm(instance=event)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return render(request, "event_form.html", {
                "form": EventForm(),  
                "message": "✅ Event Updated Successfully!"
            })
    else:
        form = EventForm(instance=event)
        

    context = {"form": form}
    return render(request, "event_form.html", context)


def delete_event(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == 'POST':
        event.delete()
        messages.success(request, "✅ Event deleted successfully!")
        return redirect('dashboard')
    
    context = {'event': event}
    return render(request, 'confirm_delete.html', context)

