from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
from .models import Event


def calendar(request):
    events = Event.objects.all()
    return render(request, 'calendar.html', {'events': events})


def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')
        event = Event.objects.create(title=title, start=start, end=end)
        return JsonResponse({'status': 'success', 'event_id': event.id})
    else:
        return JsonResponse({'status': 'fail'})


def update_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(id=event_id)
        event.title = request.POST.get('title')
        event.start = request.POST.get('start')
        event.end = request.POST.get('end')
        event.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'fail'})


def delete_event(request, event_id):
    if request.method == 'POST':
        Event.objects.filter(id=event_id).delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'fail'})
