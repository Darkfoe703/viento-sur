from .models import RecurringSchedule
from datetime import time

# CRUD - Create, Read, Update, Delete
# POST - Create
def create_schedule(day_of_week, start_time, end_time):
    """Create a new schedule.
    
    Keyword arguments:
    Schedule information.
    start_time -- Start time of the schedule
    end_time -- End time of the schedule
    day_of_week -- Day of the week (0-6)
    is_available -- Is the schedule available (default: True)
    Return: schedule -- Schedule object
    """
    
    schedule = RecurringSchedule.objects.create(
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
        is_available=True,
    )
    return schedule

# GET - Read
def get_all_recurring_schedules():
    """ Get all schedules. """
    return RecurringSchedule.objects.all()

def get_recurring_schedules_by_availability(is_available=True):
    """ Get schedule by availability. """
    return RecurringSchedule.objects.filter(is_available=is_available)

def get_recurring_schedules_by_day(day_of_week):
    """ Get schedule by day. """
    return RecurringSchedule.objects.filter(day_of_week=day_of_week)

def get_recurring_schedules_by_time_of_day(morning=True):
    """ Get schedule by time of day. """
    if morning:
        # Before 13:00 
        return RecurringSchedule.objects.filter(start_time__lt=time(13, 0))
    else:
        # After 13:00
        return RecurringSchedule.objects.filter(start_time__gte=time(13, 0))
    
def get_recurring_schedules_by_time_range(start_time=None, end_time=None):
    """ Get schedule by time range. """
    queryset = RecurringSchedule.objects.all()
    if start_time is not None:
        queryset = queryset.filter(start_time__gte=time(start_time, 0))
    if end_time is not None:
        queryset = queryset.filter(end_time__lte=time(end_time, 0))
    return queryset

# PUT - Update
# TODO: Analizar cómo actualizar un schedule

# DELETE - Delete
def delete_schedule(day_of_week, start_time):
    """Delete a schedule by day of week and start time."""

    schedule = RecurringSchedule.objects.get(
        day_of_week=day_of_week,
        start_time=start_time
    )
    schedule.delete()
    return schedule

def delete_all_recurring_schedules():
    """Delete all recurring schedules."""
    RecurringSchedule.objects.all().delete()
    return True