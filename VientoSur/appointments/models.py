from django.db import models
from patients.models import Patient
from schedules.models import RecurringSchedule


class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )
    schedule = models.ForeignKey(
        RecurringSchedule, on_delete=models.CASCADE, related_name="appointments"
    )
    start_date = models.DateField(
        auto_now_add=True
    )  # Fecha en que se asignó este horario al paciente
    end_date = models.DateField(
        null=True, blank=True
    )  # Fecha en que finaliza la asignación (alta/abandono)
    created_at = models.DateTimeField(auto_now_add=True)
    # Podrías agregar campos para el motivo de la consulta, notas, etc.

    class Meta:
        unique_together = (
            "schedule",
            "start_date",
        )  # Evita duplicados para el mismo horario en la misma fecha de inicio (podría ajustarse según tu lógica)

    def __str__(self):
        return (
            f"Cita de {self.patient} para el {self.schedule} (desde {self.start_date})"
        )

