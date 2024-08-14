from django.shortcuts import HttpResponse, get_object_or_404, render

from scheduler.models import Schedule


def index(request):
    return HttpResponse('Hello, World!')

def display_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    context = schedule.as_dict()
    return render(request, "scheduler/schedule.html", context)
