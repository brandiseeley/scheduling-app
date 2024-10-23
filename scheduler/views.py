from django.shortcuts import HttpResponse, get_object_or_404, render
from django.http import JsonResponse
from .models import SlotCluster

import json

from scheduler.models import Schedule


def index(request):
    return HttpResponse('Hello, World!')

def display_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    context = schedule.as_dict()
    return render(request, "scheduler/schedule.html", context)

def schedule_data(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    context = schedule.as_dict()
    print(context)
    return JsonResponse(context, safe=False)

def add_user_availability(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)

    try:
        data = json.loads(request.body)

        SlotCluster.objects.create(
            is_base=False,
            owner=data.get('owner'),
            slots=data.get('slots'),
            schedule=schedule,
            )
    except Exception as e:
        print('Problem happened when adding user availabiltiy')
        raise e
