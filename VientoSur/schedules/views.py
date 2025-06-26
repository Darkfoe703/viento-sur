# schedules/views.py
# TODO: Ver FIXME de serializer.py Diferenciación para POST y PUT
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import RecurringSchedule
from .serializers import RecurringScheduleSerializer
from . import services
from .filters import RecurringScheduleFilter  # 👈 NUEVO
from drf_spectacular.utils import extend_schema, OpenApiResponse

from django_filters.rest_framework import DjangoFilterBackend  # 👈 NUEVO


class RecurringScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = RecurringScheduleSerializer
    queryset = RecurringSchedule.objects.all()

    filter_backends = [DjangoFilterBackend]  # 👈 Activa filtros
    filterset_class = RecurringScheduleFilter  # 👈 Usa nuestra clase de filtros

    def get_queryset(self):
        """
        Si no se pasan filtros personalizados, devolvemos todos los horarios,
        para que se paginen los primeros 20 por defecto.
        """
        return RecurringSchedule.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                schedule = services.create_schedule(**serializer.validated_data)
                output_serializer = self.get_serializer(schedule)
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            except DjangoValidationError as e:
                raise DRFValidationError({"error": str(e)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecurringScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecurringSchedule.objects.all()
    serializer_class = RecurringScheduleSerializer

    def update(self, request, *args, **kwargs):
        schedule_id = self.get_object().id
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            updated_schedule = services.update_schedule(schedule_id, **serializer.validated_data)
            return Response(self.get_serializer(updated_schedule).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            raise DRFValidationError({"error": str(e)})


class RecurringScheduleDeleteAllView(APIView):
    @extend_schema(
        responses={
            204: OpenApiResponse(
                description="Todos los horarios fueron eliminados exitosamente."
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        services.delete_all_recurring_schedules()
        return Response(status=status.HTTP_204_NO_CONTENT)
