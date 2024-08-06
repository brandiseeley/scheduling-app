from datetime import datetime

from django.test import TestCase
from django.db.utils import IntegrityError

from .models import TimeRange

class TimeRangeTestCase(TestCase):
    """Tests for single TimeRange objects"""
    def setUp(self):
        pass

    def test_creating_range(self):
        """Creating a range with start before end works"""
        earlier = datetime(2024, 8, 4)
        later = datetime(2024, 10, 4)
        time_range = TimeRange(start_time=earlier, end_time=later)
        time_range.save()
        self.assertEqual(time_range.start_time, earlier)
        self.assertEqual(time_range.end_time, later)

    def test_creating_reversed_range(self):
        """Creating a range with end before start raises an error"""
        earlier = datetime(2024, 8, 4)
        later = datetime(2024, 10, 4)
        time_range = TimeRange(start_time=later, end_time=earlier)
        self.assertRaises(IntegrityError, time_range.save)

    def test_creating_same_start_end_range(self):
        """Creating a range with the same start and end raises an error"""
        time = datetime(2024, 8, 4)
        time_range = TimeRange(start_time=time, end_time=time)
        self.assertRaises(IntegrityError, time_range.save)
