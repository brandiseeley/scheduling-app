from django.shortcuts import HttpResponse, get_object_or_404, render
from django.forms.models import model_to_dict

from scheduler.models import Schedule, TimeRangeUnion


def index(request):
    return HttpResponse('Hello, World!')

def display_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    main_union = schedule.get_main_union()
    user_unions = schedule.get_user_unions()
    context = {
        "schedule":    model_to_dict(schedule),
        "main_union":  model_to_dict(main_union),
        "user_unions": [ model_to_dict(union) for union in user_unions ],
        }
    return render(request, "scheduler/schedule.html", context)
