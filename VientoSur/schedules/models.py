from django.db import models
from django.core.exceptions import ValidationError

class RecurringSchedule(models.Model):
    DAY_OF_WEEK_CHOICES = [
        (0, "Lunes"),
        (1, "Martes"),
        (2, "Miércoles"),
        (3, "Jueves"),
        (4, "Viernes"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    day_of_week = models.IntegerField(choices=DAY_OF_WEEK_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    is_reserved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('day_of_week', 'start_time')
        ordering = ['day_of_week', 'start_time']

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")

    def __str__(self):
        day_name = self.get_day_of_week_display()
        return f"{day_name} de {self.start_time} a {self.end_time} ({'Disponible' if self.is_available else 'No Disponible'})"
