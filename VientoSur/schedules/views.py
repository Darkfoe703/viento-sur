from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RecurringSchedule
from .serializers import RecurringScheduleSerializer
from . import services
from drf_spectacular.utils import extend_schema, OpenApiResponse


class RecurringScheduleListCreateView(generics.ListCreateAPIView):
    queryset = RecurringSchedule.objects.all()
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

    def perform_create(self, serializer):
        serializer.save()


class RecurringScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecurringSchedule.objects.all()
    serializer_class = RecurringScheduleSerializer

class RecurringScheduleDeleteAllView(APIView):
    @extend_schema(
        responses={
            204: OpenApiResponse(description="No content")
        }
    )
    def delete(self, request, *args, **kwargs):
        services.delete_all_recurring_schedules()
        return Response(status=status.HTTP_204_NO_CONTENT)
