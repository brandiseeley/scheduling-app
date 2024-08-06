from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint

class TimeRange(models.Model):
    """A range that spans from one time to another"""
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')

    def __add__(self, other):
        """Returns a new TimeRange object using the earlier start and the later stop time"""
        if not isinstance(other, TimeRange):
            return NotImplemented
        new_start = self.start_time if self.start_time < other.start_time else other.start_time
        new_end = self.end_time if self.end_time > other.end_time else other.end_time
        return TimeRange(start_time=new_start, end_time=new_end)

    def __lt__(self, other):
        """A TimeRange with a start time that is earlier than other will be considered less than"""
        if not isinstance(other, TimeRange):
            return NotImplemented
        if self.start_time == other.start_time:
            return self.end_time < other.end_time
        else:
            return self.start_time < other.start_time

    def __eq__(self, other):
        """Both start and end times must be the same to be considered equal"""
        if not isinstance(other, TimeRange):
            return NotImplemented
        return self.start_time == other.start_time and self.end_time == other.end_time

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
