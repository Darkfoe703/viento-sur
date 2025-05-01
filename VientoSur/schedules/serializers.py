from rest_framework import serializers
from .models import RecurringSchedule


class RecurringScheduleSerializer(serializers.ModelSerializer):
    day_of_week = serializers.ChoiceField(choices=RecurringSchedule.DAY_OF_WEEK_CHOICES)

    class Meta:
        model = RecurringSchedule
        fields = "__all__"
        # O: fields = ('day_of_week', 'start_time', 'end_time')
