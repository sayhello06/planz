from django.shortcuts import render
from django.http import JsonResponse
from calendarApp.models import Event


def calendar(request):
    all_events = Event.objects.all()
    context = {
        "events": all_events,
    }
    return render(request, 'calendarApp/calendar.html', context)


def all_events(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start.strftime("%Y-%m-%d %H:%M"),
            'end': event.end.strftime("%Y-%m-%d %H:%M"),
        })
    return JsonResponse(event_list, safe=False)

def add_event(request):
    title = request.GET.get('title', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    event = Event(title=title, start=start, end=end)
    event.save()
    return JsonResponse({'success': True})

def update_event(request):
    id = request.GET.get('id', None)
    title = request.GET.get('title', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    event = Event.objects.get(id=id)
    event.title = title
    event.start = start
    event.end = end
    event.save()
    return JsonResponse({'success': True})

def remove_event(request):
    id = request.GET.get('id', None)
    event = Event.objects.get(id=id)
    event.delete()
    return JsonResponse({'success': True})