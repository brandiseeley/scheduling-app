from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('schedules/<int:schedule_id>', views.display_schedule, name="display schedule"),
    path('schedules/data/<int:schedule_id>', views.schedule_data, name="schedule data"),
]