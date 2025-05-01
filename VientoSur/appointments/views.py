from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Appointment
from .serializers import AppointmentSerializer
from . import services


class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            patient_id = serializer.validated_data.pop("patient_id")
            schedule_id = serializer.validated_data.pop("schedule_id")
            appointment = services.create_appointment(
                patient_id=patient_id,
                schedule_id=schedule_id,
                **serializer.validated_data  # Pass other validated data (start_date, end_date if allowed)
            )
            appointment_serializer = self.get_serializer(appointment)
            return Response(appointment_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AppointmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if services.delete_appointment(instance.id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AppointmentDeleteAllView(APIView):

    @extend_schema(
            responses={
                204: OpenApiResponse(description="No content")
                }
            )
    def delete(self, request, *args, **kwargs):
        services.delete_all_appointments()
        return Response(status=status.HTTP_204_NO_CONTENT)
