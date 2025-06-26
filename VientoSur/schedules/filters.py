# schedules/filters.py

import django_filters
from django_filters.rest_framework import FilterSet
from .models import RecurringSchedule

# Diccionario auxiliar para traducir nombres de días a números
DAY_NAME_TO_INT = {
    "lunes": 0,
    "martes": 1,
    "miércoles": 2,
    "miercoles": 2,
    "jueves": 3,
    "viernes": 4,
    "sábado": 5,
    "sabado": 5,
    "domingo": 6,
}

class RecurringScheduleFilter(FilterSet):
    # Filtros estándar
    start_time = django_filters.TimeFilter(field_name="start_time", lookup_expr="gte")
    end_time = django_filters.TimeFilter(field_name="end_time", lookup_expr="lte")
    is_available = django_filters.BooleanFilter(field_name="is_available")
    is_reserved = django_filters.BooleanFilter(field_name="is_reserved")

    # Filtros personalizados
    day_name = django_filters.CharFilter(method="filter_by_day_name")
    time_of_day = django_filters.CharFilter(method="filter_by_time_of_day")

    class Meta:
        model = RecurringSchedule
        fields = [
            "day_name",
            "time_of_day",
            "start_time",
            "end_time",
            "is_available",
            "is_reserved",
        ]

    def filter_by_day_name(self, queryset, name, value):
        """Filtra por nombre del día (lunes, martes...)"""
        day_index = DAY_NAME_TO_INT.get(value.lower())
        if day_index is not None:
            return queryset.filter(day_of_week=day_index)
        return queryset.none()  # Si el nombre no es válido, no devuelve resultados

    def filter_by_time_of_day(self, queryset, name, value):
        """Filtra por turno (morning / afternoon)"""
        from datetime import time

        if value.lower() == "morning":
            return queryset.filter(
                start_time__gte=time(7, 0), start_time__lt=time(13, 0)
            )
        elif value.lower() == "afternoon":
            return queryset.filter(
                start_time__gte=time(13, 0), start_time__lte=time(21, 0)
            )
        return queryset
