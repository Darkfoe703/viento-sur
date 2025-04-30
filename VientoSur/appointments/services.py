from .models import Appointment


# CRUD - Create, Read, Update, Delete
# POST - Create
def create_appointment(patient, schedule, start_date):
    """Create a new appointment.

    Keyword arguments:
    Appointment information.
    patient -- Patient object
    schedule -- Schedule object
    start_date -- Start date of the appointment
    Return: appointment -- Appointment object
    """

    appointment = Appointment.objects.create(
        patient=patient,
        schedule=schedule,
        start_date=start_date,
    )
    return appointment

# GET - Read
def get_all_appointments():
    """ Get all appointments. """
    return Appointment.objects.all()

def get_appointment_by_patient(patient):
    """ Get appointment by patient. """
    return Appointment.objects.filter(patient=patient)

def get_appointment_by_schedule(schedule):
    """ Get appointment by schedule. """
    return Appointment.objects.filter(schedule=schedule)

def get_appointment_by_date(start_date):
    """ Get appointment by date. """
    return Appointment.objects.filter(start_date=start_date)

def get_appointment_by_date_range(start_date=None, end_date=None):
    """ Get appointment by date range. """
    queryset = Appointment.objects.all()
    if start_date is not None:
        queryset = queryset.filter(start_date__gte=start_date)
    if end_date is not None:
        queryset = queryset.filter(end_date__lte=end_date)
    return queryset

# PUT - Update
# TODO: Analizar cómo actualizar un appointment

# DELETE - Delete
def delete_appointment(patient, schedule):
    """Delete an appointment by patient and schedule."""
    appointment = Appointment.objects.get(patient=patient, schedule=schedule)
    appointment.delete()
    return appointment