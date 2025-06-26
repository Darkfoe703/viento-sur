from rest_framework import serializers
from .models import RecurringSchedule

# FIXME: Diferenciar serializador de creación y actualización
#       y diferenciar validaciones.

class RecurringScheduleSerializer(serializers.ModelSerializer):
    day_of_week = serializers.ChoiceField(choices=RecurringSchedule.DAY_OF_WEEK_CHOICES, required=False)

    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    is_available = serializers.BooleanField(required=False)
    is_reserved = serializers.BooleanField(required=False)

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

        # Solo validar unicidad si tenemos ambos campos
        if day is not None and start is not None:
            if self.instance is None:
                # Crear nuevo
                exists = RecurringSchedule.objects.filter(
                    day_of_week=day, start_time=start
                ).exists()
                if exists:
                    raise serializers.ValidationError(
                        "Ya existe un horario con ese día y hora de inicio."
                    )
            else:
                # Actualización parcial o completa
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
