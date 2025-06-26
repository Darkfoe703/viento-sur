from .models import RecurringSchedule
from datetime import time
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist


# CREATE
def create_schedule(
    day_of_week, start_time, end_time, is_available=True, is_reserved=False
):
    """
    Create a new schedule.

    Raises:
        ValidationError: si ya existe un horario con el mismo día y hora de inicio,
        o si la hora de inicio es mayor o igual a la de fin.
    """
    if start_time >= end_time:
        raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")

    try:
        schedule = RecurringSchedule.objects.create(
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            is_available=is_available,
            is_reserved=is_reserved,
        )
        return schedule
    except IntegrityError:
        raise ValidationError("Ya existe un horario con ese día y hora de inicio.")


# READ
def get_all_recurring_schedules():
    return RecurringSchedule.objects.all()


def get_recurring_schedules_by_availability(is_available=True):
    return RecurringSchedule.objects.filter(is_available=is_available)


def get_recurring_schedules_by_day(day_of_week):
    return RecurringSchedule.objects.filter(day_of_week=day_of_week)


def get_recurring_schedules_by_time_of_day(morning=True):
    if morning:
        return RecurringSchedule.objects.filter(start_time__lt=time(13, 0))
    return RecurringSchedule.objects.filter(start_time__gte=time(13, 0))


def get_recurring_schedules_by_time_range(start_time=None, end_time=None):
    queryset = RecurringSchedule.objects.all()
    if start_time is not None:
        queryset = queryset.filter(start_time__gte=time(start_time, 0))
    if end_time is not None:
        queryset = queryset.filter(end_time__lte=time(end_time, 0))
    return queryset



# UPDATE
def update_schedule(
    schedule_id,
    day_of_week=None,
    start_time=None,
    end_time=None,
    is_available=None,
    is_reserved=None,
):
    """
    Update a schedule by its ID.

    Raises:
        ValidationError: si no se encuentra el horario o si los datos son inválidos.
    """
    try:
        schedule = RecurringSchedule.objects.get(id=schedule_id)
    except RecurringSchedule.DoesNotExist:
        raise ValidationError("El horario especificado no existe.")

    # Validación de horario
    if start_time is not None and end_time is not None:
        if start_time >= end_time:
            raise ValidationError("La hora de fin debe ser posterior a la de inicio.")

    # Simular los nuevos valores para verificar unicidad
    new_day = day_of_week if day_of_week is not None else schedule.day_of_week
    new_start = start_time if start_time is not None else schedule.start_time

    conflict = (
        RecurringSchedule.objects.exclude(id=schedule.id)
        .filter(day_of_week=new_day, start_time=new_start)
        .exists()
    )
    if conflict:
        raise ValidationError("Ya existe otro horario con ese día y hora de inicio.")

    # Actualización condicional
    if day_of_week is not None:
        schedule.day_of_week = day_of_week
    if start_time is not None:
        schedule.start_time = start_time
    if end_time is not None:
        schedule.end_time = end_time
    if is_available is not None:
        schedule.is_available = is_available
    if is_reserved is not None:
        schedule.is_reserved = is_reserved

    schedule.save()
    return schedule


# DELETE
def delete_schedule(day_of_week, start_time):
    """
    Delete a schedule by its day and start time.

    Raises:
        ValidationError: si el horario no existe.
    """
    try:
        schedule = RecurringSchedule.objects.get(
            day_of_week=day_of_week, start_time=start_time
        )
        schedule.delete()
        return True
    except RecurringSchedule.DoesNotExist:
        raise ValidationError("No se encontró el horario para eliminar.")


def delete_all_recurring_schedules():
    RecurringSchedule.objects.all().delete()
    return True
