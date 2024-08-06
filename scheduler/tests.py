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
        self.assertEqual(earlier, time_range.start_time)
        self.assertEqual(later, time_range.end_time)

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

    def test_less_than(self):
        """A TimeRange with an earlier start is considered less than a TimeRange with a later start"""
        time1 = datetime(2024, 8, 6, 7, 30)
        time2 = datetime(2024, 8, 6, 8, 30)
        time3 = datetime(2024, 8, 6, 9, 30)
        time4 = datetime(2024, 8, 6, 10, 30)

        range1 = TimeRange(start_time=time1, end_time=time3)
        range2 = TimeRange(start_time=time2, end_time=time4)
        self.assertLess(range1, range2)

    def test_equal(self):
        """Two TimeRanges are equal if they have the same start and stop"""
        start1 = datetime(2024, 8, 6, 7, 30)
        start2 = datetime(2024, 8, 6, 7, 30)
        stop1 = datetime(2024, 8, 6, 8, 30)
        stop2 = datetime(2024, 8, 6, 8, 30)
        range1 = TimeRange(start_time=start1, end_time=stop1)
        range2 = TimeRange(start_time=start2, end_time=stop2)
        self.assertEqual(range1, range2)

    def test_not_equal(self):
        """Two TimeRanges with the same starts but different stops are not equal"""
        start = datetime(2024, 8, 6, 7, 30)
        stop1 = datetime(2024, 8, 6, 8, 30)
        stop2 = datetime(2024, 8, 6, 9, 30)
        range1 = TimeRange(start_time=start, end_time=stop1)
        range2 = TimeRange(start_time=start, end_time=stop2)
        self.assertNotEqual(range1, range2)
        
    def test_add_with_overlap(self):
        """Adding two overlapping time ranges gives a larger range"""
        time1 = datetime(2024, 8, 6, 7, 30)
        time2 = datetime(2024, 8, 6, 8, 30)
        time3 = datetime(2024, 8, 6, 9, 30)
        time4 = datetime(2024, 8, 6, 10, 30)
        range1 = TimeRange(start_time=time1, end_time=time3)
        range2 = TimeRange(start_time=time2, end_time=time4)

        new_range = range1 + range2
        self.assertEqual(time1, new_range.start_time)
        self.assertEqual(time4, new_range.end_time)

    def test_add_without_overlap(self):
        """Adding two non-overlapping time ranges gives a larger range"""
        time1 = datetime(2024, 8, 6, 7, 30)
        time2 = datetime(2024, 8, 6, 8, 30)
        time3 = datetime(2024, 8, 6, 9, 30)
        time4 = datetime(2024, 8, 6, 10, 30)
        range1 = TimeRange(start_time=time1, end_time=time2)
        range2 = TimeRange(start_time=time3, end_time=time4)

        new_range = range1 + range2
        self.assertEqual(time1, new_range.start_time)
        self.assertEqual(time4, new_range.end_time)
