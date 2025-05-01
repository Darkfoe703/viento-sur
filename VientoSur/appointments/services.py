# appointments/services.py
from .models import Appointment
from schedules.models import RecurringSchedule
from patients.models import Patient


def create_appointment(patient_id, schedule_id, start_date=None, end_date=None):
    """Create a new appointment and mark the schedule as unavailable."""
    try:
        patient = Patient.objects.get(pk=patient_id)
        schedule = RecurringSchedule.objects.get(pk=schedule_id)
    except Patient.DoesNotExist:
        raise ValueError(f"No existe el paciente con ID: {patient_id}")
    except RecurringSchedule.DoesNotExist:
        raise ValueError(f"No existe el horario con ID: {schedule_id}")

    if not schedule.is_available:
        raise ValueError(f"El horario con ID: {schedule_id} no está disponible.")

    appointment = Appointment.objects.create(
        patient=patient, schedule=schedule, start_date=start_date, end_date=end_date
    )

    # Set the schedule as unavailable
    schedule.is_available = False
    schedule.save()

    return appointment


def get_all_appointments():
    """Get all appointments."""
    return Appointment.objects.all()


def get_appointment_by_id(appointment_id):
    """Get an appointment by its ID."""
    try:
        return Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        return None


def update_appointment(appointment_id, data):
    """Update an appointment."""
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
        # Lógica para actualizar los campos de la cita
        for key, value in data.items():
            setattr(appointment, key, value)
        appointment.save()
        return appointment
    except Appointment.DoesNotExist:
        return None


def delete_appointment(appointment_id):
    """Delete an appointment and mark the schedule as available."""
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
        schedule = appointment.schedule
        appointment.delete()
        # Marcar el horario como disponible
        schedule.is_available = True
        schedule.save()
        return True
    except Appointment.DoesNotExist:
        return False


def delete_all_appointments(): #TODO: en ingles
    """Elimina todas las citas y marca todos los horarios recurrentes como disponibles."""
    appointments = Appointment.objects.all()
    schedule_ids = set(appointment.schedule_id for appointment in appointments)
    Appointment.objects.all().delete()

    # Marcar todos los horarios que estaban asociados a alguna cita como disponibles
    RecurringSchedule.objects.filter(id__in=list(schedule_ids)).update(
        is_available=True
    )
    return True
