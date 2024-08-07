from datetime import datetime

from scheduler.models import TimeRange, TimeRangeUnion, Schedule

# Create the main schedule
schedule = Schedule.objects.create(title="Meeting Next Week")
schedule.save()

monday = datetime(2024, 9, 2, 7)
friday = datetime(2024, 9, 6, 17)
main_range = TimeRange.objects.create(start_time=monday, end_time=friday)
main_range.save()

main_union = TimeRangeUnion.objects.create(is_main=True)
schedule.add_main_union(main_union)

# Create a user union

# Create ranges
tuesday_morning = datetime(2024, 9, 3, 8)
tuesday_noon = datetime(2024, 9, 3, 12)
tuesday_range = TimeRange.objects.create(start_time=tuesday_morning, end_time=tuesday_noon)

thursday_noon = datetime(2024, 9, 5, 12)
thursday_evening = datetime(2024, 9, 5, 17)
thursday_range = TimeRange.objects.create(start_time=thursday_noon, end_time=thursday_evening)

# Create union for user
user1_union = TimeRangeUnion.objects.create(is_main=False, owner='Brandi')
user1_union.add_range(tuesday_range)
user1_union.add_range(thursday_range)

# Add user union to schedule
schedule.add_user_union(user1_union)
