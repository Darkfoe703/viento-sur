from .models import Patient

# CRUD - Create, Read, Update, Delete

# POST - CREATE
def create_patient(creation_date, name, last_name, age, birth_date, email, phone_number):
    """Create a new patient.
    
    Keyword arguments:
    Patient personal information.
    Return: patinet -- Patient object
    """
    patient = Patient.objects.create(
        creation_date=creation_date,
        name=name,
        last_name=last_name,
        age=age,
        birth_date=birth_date,
        email=email,
        phone_number=phone_number
    )
    # Acá puedo agregar lñogica adicional despues de crear el paciente
    # Por ejemplo, enviar un correo de bienvenida al paciente
    return patient

# GET - READ
def get_all_patients():
    """Get all patients."""
    return Patient.objects.all()

def get_patient_by_id(patient_id):
    """Get a patient by ID."""
    try:
        return Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        return None

def get_patient_by_name(name):
    """Get a patient by string in name (case-insensitive)."""
    return Patient.objects.filter(name__icontains=name)

def get_patient_by_last_name(last_name):
    """Get a patient by string in last name."""
    return Patient.objects.filter(last_name__icontains=last_name)

def  get_patient_by_full_name(name=None, last_name=None):
    """Get a patient by string in name and last name (case-insensitive)."""
    queryset = Patient.objects.all()
    if name:
        queryset = queryset.filter(name__icontains=name)
    if last_name:
        queryset = queryset.filter(last_name__icontains=last_name)
    return queryset

# PUT - UPDATE
def update_patient(patient_id, data):
    """Update a patient by ID."""
    try:
        patient = Patient.objects.get(pk=patient_id)
        for key, value in data.items():
            setattr(patient, key, value)
        patient.save()
        return patient
    except Patient.DoesNotExist:
        return None

# DELETE -
def delete_patient(patient_id):
    """Delete a patient by ID."""
    try:
        patient = Patient.objects.get(pk=patient_id)
        patient.delete()
        return True # Patient deleted successfully
    except Patient.DoesNotExist:
        return False


def delete_all_patients():
    """Delete all patients."""
    Patient.objects.all().delete()
    return True
