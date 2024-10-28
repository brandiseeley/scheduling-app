from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('schedules/new', views.new_schedule, name="new schedule"),
    path('schedules/<int:schedule_id>', views.display_schedule, name="display schedule"),
    path('schedules/<int:schedule_id>/data', views.schedule_data, name="schedule data"),
    path('schedules/<int:schedule_id>/add_user', views.add_user_availability, name="add user"),
]