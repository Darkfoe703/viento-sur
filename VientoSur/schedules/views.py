from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from .models import RecurringSchedule
from .serializers import RecurringScheduleSerializer
from . import services
from drf_spectacular.utils import extend_schema, OpenApiResponse


class RecurringScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = RecurringScheduleSerializer

    def get_queryset(self):
        day = self.request.query_params.get("day")
        time_of_day = self.request.query_params.get("time_of_day")

        if day:
            return services.get_recurring_schedules_by_day(day)
        elif time_of_day == "morning":
            return services.get_recurring_schedules_by_time_of_day(morning=True)
        elif time_of_day == "afternoon":
            return services.get_recurring_schedules_by_time_of_day(morning=False)
        return services.get_all_recurring_schedules()

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
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            try:
                updated_schedule = services.update_schedule(
                    day_of_week=serializer.validated_data["day_of_week"],
                    start_time=serializer.validated_data["start_time"],
                    end_time=serializer.validated_data.get("end_time"),
                    is_available=serializer.validated_data.get("is_available"),
                    is_reserved=serializer.validated_data.get("is_reserved"),
                )
                return Response(
                    self.get_serializer(updated_schedule).data,
                    status=status.HTTP_200_OK,
                )
            except DjangoValidationError as e:
                raise DRFValidationError({"error": str(e)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            services.delete_schedule(
                day_of_week=instance.day_of_week, start_time=instance.start_time
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DjangoValidationError as e:
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
