from rest_framework import serializers
from .models import Appointment
from patients.serializers import PatientSerializer
from schedules.serializers import RecurringScheduleSerializer
from schedules.models import RecurringSchedule
from patients.models import Patient


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    schedule = RecurringScheduleSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    schedule_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("id", "created_at", "patient", "schedule", "start_date")

    def validate(self, data):
        schedule_id = data.get("schedule_id")  # Usamos .get() para evitar KeyError
        if (
            schedule_id is not None
            and Appointment.objects.filter(
                schedule_id=schedule_id, end_date__isnull=True
            ).exists()
        ):
            raise serializers.ValidationError("Este horario ya está ocupado.")
        return data

    def create(self, validated_data):
        patient_id = validated_data.pop("patient_id")
        schedule_id = validated_data.pop("schedule_id")
        patient = Patient.objects.get(pk=patient_id)
        schedule = RecurringSchedule.objects.get(pk=schedule_id)
        appointment = Appointment.objects.create(
            patient=patient, schedule=schedule, **validated_data
        )
        return appointment

    def update(self, instance, validated_data):
        patient_id = validated_data.pop("patient_id", instance.patient.id)
        schedule_id = validated_data.pop("schedule_id", instance.schedule.id)
        instance.patient = Patient.objects.get(id=patient_id)
        instance.schedule = RecurringSchedule.objects.get(id=schedule_id)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
