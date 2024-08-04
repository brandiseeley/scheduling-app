from datetime import datetime

from django.test import TestCase
from django.db.utils import IntegrityError

from .models import TimeRange

class TimeRangeTestCase(TestCase):
    def setUp(self):
        pass

    def test_creating_reversed_range(self):
        """Creating a range with end before start raises an error"""
        earlier = datetime(2024, 8, 4)
        later = datetime(2024, 10, 4)
        time_range = TimeRange(start_time=later, end_time=later)
        self.assertRaises(IntegrityError, time_range.save)
