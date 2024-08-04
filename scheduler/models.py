from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint

class TimeRange(models.Model):
    """A range that spans from one time to another"""
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')

    def __add__(self, other):
        """Returns a new TimeRange object merging the two times if they overlap. None if they don't"""
        pass

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(start_time__lt=models.F('end_time')),
                name='check_start_time_before_end_time'
            ),
        ]

class Schedule(models.Model):
    """The main schedule that is shared between users to add availability"""
    title = models.CharField(max_length=300)
    timeRange = models.ForeignKey(TimeRange, on_delete=models.CASCADE)