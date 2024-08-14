from datetime import datetime
from zoneinfo import ZoneInfo

from django.test import TestCase
from django.db.utils import IntegrityError

from .models import Schedule
from .models import TimeRange
from .models import TimeRangeUnion

class TimeRangeTestCase(TestCase):
    """Tests for single TimeRange objects"""
    def setUp(self):
        pass

    def test_creating_range(self):
        """Creating a range with start before end works"""
        earlier = datetime(2024, 8, 4, tzinfo=ZoneInfo('Asia/Seoul'))
        later = datetime(2024, 10, 4, tzinfo=ZoneInfo('Asia/Seoul'))
        time_range = TimeRange(start_time=earlier, end_time=later)
        time_range.save()
        self.assertEqual(earlier, time_range.start_time)
        self.assertEqual(later, time_range.end_time)

    def test_creating_reversed_range(self):
        """Creating a range with end before start raises an error"""
        earlier = datetime(2024, 8, 4, tzinfo=ZoneInfo('Asia/Seoul'))
        later = datetime(2024, 10, 4, tzinfo=ZoneInfo('Asia/Seoul'))
        time_range = TimeRange(start_time=later, end_time=earlier)
        self.assertRaises(IntegrityError, time_range.save)

    def test_creating_same_start_end_range(self):
        """Creating a range with the same start and end raises an error"""
        time = datetime(2024, 8, 4, tzinfo=ZoneInfo('Asia/Seoul'))
        time_range = TimeRange(start_time=time, end_time=time)
        self.assertRaises(IntegrityError, time_range.save)

    def test_less_than(self):
        """A TimeRange with an earlier start is less than a TimeRange with a later start"""
        time1 = datetime(2024, 8, 6, 7, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time2 = datetime(2024, 8, 6, 8, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time3 = datetime(2024, 8, 6, 9, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time4 = datetime(2024, 8, 6, 10, 30, tzinfo=ZoneInfo('Asia/Seoul'))

        range1 = TimeRange(start_time=time1, end_time=time3)
        range2 = TimeRange(start_time=time2, end_time=time4)
        self.assertLess(range1, range2)

    def test_equal(self):
        """Two TimeRanges are equal if they have the same start and stop"""
        start1 = datetime(2024, 8, 6, 7, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        start2 = datetime(2024, 8, 6, 7, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        stop1 = datetime(2024, 8, 6, 8, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        stop2 = datetime(2024, 8, 6, 8, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        range1 = TimeRange(start_time=start1, end_time=stop1)
        range2 = TimeRange(start_time=start2, end_time=stop2)
        self.assertEqual(range1, range2)

    def test_not_equal(self):
        """Two TimeRanges with the same starts but different stops are not equal"""
        start = datetime(2024, 8, 6, 7, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        stop1 = datetime(2024, 8, 6, 8, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        stop2 = datetime(2024, 8, 6, 9, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        range1 = TimeRange(start_time=start, end_time=stop1)
        range2 = TimeRange(start_time=start, end_time=stop2)
        self.assertNotEqual(range1, range2)

    def test_add_with_overlap(self):
        """Adding two overlapping time ranges gives a larger range"""
        time1 = datetime(2024, 8, 6, 7, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time2 = datetime(2024, 8, 6, 8, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time3 = datetime(2024, 8, 6, 9, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time4 = datetime(2024, 8, 6, 10, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        range1 = TimeRange(start_time=time1, end_time=time3)
        range2 = TimeRange(start_time=time2, end_time=time4)

        new_range = range1 + range2
        self.assertEqual(time1, new_range.start_time)
        self.assertEqual(time4, new_range.end_time)

    def test_add_without_overlap(self):
        """Adding two non-overlapping time ranges gives a larger range"""
        time1 = datetime(2024, 8, 6, 7, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time2 = datetime(2024, 8, 6, 8, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time3 = datetime(2024, 8, 6, 9, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time4 = datetime(2024, 8, 6, 10, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        range1 = TimeRange(start_time=time1, end_time=time2)
        range2 = TimeRange(start_time=time3, end_time=time4)

        new_range = range1 + range2
        self.assertEqual(time1, new_range.start_time)
        self.assertEqual(time4, new_range.end_time)

    def test_sorting_ranges_without_overlap(self):
        """Sorting a list of ranges should result in ascending start times"""
        time1 = datetime(2024, 8, 6, 7, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time2 = datetime(2024, 8, 6, 8, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time3 = datetime(2024, 8, 6, 9, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        time4 = datetime(2024, 8, 6, 10, 30, tzinfo=ZoneInfo('Asia/Seoul'))
        range1 = TimeRange(start_time=time1, end_time=time2)
        range2 = TimeRange(start_time=time3, end_time=time4)

        range_list = [range2, range1]
        self.assertEqual([range1, range2], sorted(range_list))


class ScheduleCreationTestCase(TestCase):
    def test_schedule_must_have_title(self):
        pass

    def test_cannot_have_multiple_main_ranges(self):
        pass

    def test_cannot_add_user_range_without_main_range(self):
        pass

    def test_add_range_within_bounds(self):
        pass

    def test_cannot_add_range_out_side_of_main_range_bounds(self):
        pass

    def test_can_add_multiple_user_ranges(self):
        pass

class ScheduleFunctionalityTestCase(TestCase):
    """Tests for Schedule models"""
    def setUp(self):
        timezone = ZoneInfo('Asia/Seoul')

        # Create Schedule and it's main range
        schedule = Schedule.objects.create(title="Meeting Next Week")
        schedule.save()

        monday = datetime(2024, 9, 2, 7, tzinfo=timezone)
        friday = datetime(2024, 9, 6, 17, tzinfo=timezone)
        main_range = TimeRange.objects.create(start_time=monday, end_time=friday)
        main_range.save()

        main_union = TimeRangeUnion.objects.create(is_main=True)
        main_union.add_range(main_range)
        schedule.add_main_union(main_union)

        # Create ranges for user
        tuesday_morning = datetime(2024, 9, 3, 8, tzinfo=timezone)
        tuesday_noon =    datetime(2024, 9, 3, 12, tzinfo=timezone)
        tuesday_range = TimeRange.objects.create(start_time=tuesday_morning, end_time=tuesday_noon)
        tuesday_range.save()

        thursday_noon =    datetime(2024, 9, 5, 12, tzinfo=timezone)
        thursday_evening = datetime(2024, 9, 5, 17, tzinfo=timezone)
        thursday_range = TimeRange.objects.create(start_time=thursday_noon, end_time=thursday_evening)
        thursday_range.save()

        # Create union for user
        user1_union = TimeRangeUnion.objects.create(is_main=False, owner='Brandi')
        user1_union.add_range(tuesday_range)
        user1_union.add_range(thursday_range)

        # Add user union to schedule
        schedule.add_user_union(user1_union)

        self.__class__.schedule = schedule

    def test_days_property(self):
        pass

    def test_hours_property(self):
        pass

    def test_add_user_union(self):
        pass
