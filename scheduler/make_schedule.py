from datetime import datetime
from zoneinfo import ZoneInfo

from scheduler.models import TimeRange, TimeRangeUnion, Schedule

# Define the timezone
timezone = ZoneInfo('UTC')

# Create the main schedule
schedule = Schedule.objects.create(title="Meeting Next Week")
schedule.save()

monday = datetime(2024, 9, 2, 7, tzinfo=timezone)
friday = datetime(2024, 9, 6, 17, tzinfo=timezone)
main_range = TimeRange.objects.create(start_time=monday, end_time=friday)
main_range.save()

main_union = TimeRangeUnion.objects.create(is_main=True)
main_union.add_range(main_range)
schedule.add_main_union(main_union)

# Create a user union

# Create ranges
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

# time1 = datetime(2024, 8, 6, 7, 30, tzinfo=timezone)
# time2 = datetime(2024, 8, 6, 8, 30, tzinfo=timezone)
# time3 = datetime(2024, 8, 6, 9, 30, tzinfo=timezone)
# time4 = datetime(2024, 8, 6, 10, 30, tzinfo=timezone)

# range1 = TimeRange(start_time=time2, end_time=time3)
# range1.save()
# range2 = TimeRange(start_time=time1, end_time=time4)
# range2.save()

# union = TimeRangeUnion.objects.create(is_main=False, owner='Brandi')
# union.add_range(range2)
# union.add_range(range1)
