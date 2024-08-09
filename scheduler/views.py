from django.shortcuts import HttpResponse, get_object_or_404, render

from scheduler.models import Schedule


def index(request):
    return HttpResponse('Hello, World!')

def display_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    main_union = schedule.main_union
    user_unions = schedule.user_unions
    context = {
        "schedule":    schedule,
        "main_union":  main_union,
        "user_unions": user_unions,
        }
    return render(request, "scheduler/schedule.html", context)
