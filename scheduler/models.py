from datetime import datetime, timedelta

from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint

class ScheduleError(Exception):
    pass

class Schedule(models.Model):
    """The main schedule that is shared between users to add availability"""
    title = models.CharField(max_length=300)

    def add_user_union(self, time_range_union):
        """Adds a new range union associated with a user"""
        self.timerangeunion_set.add(time_range_union)

    def add_main_union(self, time_range_union):
        """Adds the main range that indicates where child ranges may exist"""
        # TODO: Make sure we don't already have a 'main' union
        if self.main_union:
            raise ScheduleError('Schedule may only have one main union')

        self.timerangeunion_set.add(time_range_union)

    @property
    def main_union(self):
        try:
            main = self.timerangeunion_set.get(is_main=True)
        except TimeRangeUnion.DoesNotExist:
            return None

        return main

    @property
    def user_unions(self):
        return self.timerangeunion_set.filter(is_main=False)
    
    @property
    def days(self):
        return self.main_union.days
    
    @property
    def hours(self):
        return self.main_union.hours
    
    def as_dict(self):
        return {
            'self': self,
            'main_union':  self.main_union,
            'user_unions': self.user_unions,
            'days': self.days,
            'hour_samples': sorted(list(self.main_union.hours)),
            'user_slots': [ union.slots for union in self.user_unions ],
        }

class TimeRangeUnion(models.Model):
    """A collection of TimeRange objects representing one set of time"""
    is_main = models.BooleanField()
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.CharField(max_length=100)

    def add_range(self, time_range):
        self.timerange_set.add(time_range)

    @property
    def all_ranges(self):
        return self.timerange_set.all()

    @property
    def earliest_range(self):
        all_ranges = self.all_ranges
        return None if len(all_ranges) == 0 else all_ranges[0]

    @property
    def latest_range(self):
        return sorted(self.all_ranges, key=lambda r: r.end_time, reverse=True)[0]

    @property
    def start_date(self):
        return self.earliest_range.start_time.date()

    @property
    def end_date(self):
        return self.latest_range.end_time.date()
    
    @property
    def days(self):
        current_day = self.start_date
        days = []
        while current_day <= self.end_date:
            days.append(current_day)
            current_day += timedelta(days=1)
        return days
    
    @property
    def hours(self):
        hours = set()
        datetimes = []
        for slot in self.slots:
            hour = f'{slot.hour}:{slot.minute}'
            if hour not in hours:
                datetimes.append(slot)
            hours.add(hour)
        return datetimes

    @property
    def slots(self):
        all_slots = []
        for time_range in self.all_ranges:
            all_slots.extend(time_range.slots)
        return all_slots

class TimeRange(models.Model):
    """A range that spans from one time to another"""
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    time_range_union = models.ForeignKey(
        TimeRangeUnion,
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    @property
    def slots(self):
        all_slots = []
        
        current = self.start_time
        while current < self.end_time:
            all_slots.append(current)
            current += timedelta(minutes=30)

        return all_slots

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

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        start_string = self.start_time.strftime("%a, %d. %b %y %I:%M%p")
        end_string = self.end_time.strftime("%a, %d %b %y %I:%M%p")
        return f'TimeRange: {start_string} -to- {end_string}'

    class Meta:
        """Implements a constraint requiring start_time to preceed end_time"""
        constraints = [
            CheckConstraint(
                check=Q(start_time__lt=models.F('end_time')),
                name='check_start_time_before_end_time'
            ),
        ]
