from django.db import models


class RecurringSchedule(models.Model):
    day_of_week = models.IntegerField(
        choices=[
            (0, "Lunes"),
            (1, "Martes"),
            (2, "Miércoles"),
            (3, "Jueves"),
            (4, "Viernes"),
            (5, "Sábado"),
            (6, "Domingo"),
        ],
        default=0, blank=False
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        day_name = self.get_day_of_week_display()
        return f"{day_name} de {self.start_time} a {self.end_time}"
