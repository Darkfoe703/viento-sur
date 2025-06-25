from rest_framework import serializers
from .models import RecurringSchedule


class RecurringScheduleSerializer(serializers.ModelSerializer):
    day_of_week = serializers.ChoiceField(choices=RecurringSchedule.DAY_OF_WEEK_CHOICES)

    class Meta:
        model = RecurringSchedule
        fields = "__all__"

    def validate(self, data):
        start = data.get("start_time")
        end = data.get("end_time")

        if start and end and start >= end:
            raise serializers.ValidationError(
                "La hora de inicio debe ser anterior a la hora de fin."
            )

        day = data.get("day_of_week")

        # Para creación: verificar duplicado
        if self.instance is None:
            exists = RecurringSchedule.objects.filter(
                day_of_week=day, start_time=start
            ).exists()
            if exists:
                raise serializers.ValidationError(
                    "Ya existe un horario con ese día y hora de inicio."
                )
        else:
            # Para update: verificar que no duplique otro horario
            exists = (
                RecurringSchedule.objects.exclude(id=self.instance.id)
                .filter(day_of_week=day, start_time=start)
                .exists()
            )
            if exists:
                raise serializers.ValidationError(
                    "Otro horario ya existe con ese día y hora de inicio."
                )

        return data

    def to_representation(self, instance):
        """Personaliza la salida: día en texto en lugar de número."""
        representation = super().to_representation(instance)
        representation["day_of_week_display"] = instance.get_day_of_week_display()
        return representation
