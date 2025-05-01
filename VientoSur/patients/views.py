from django.shortcuts import render

# Create your views here.
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Patient
from .serializers import PatientSerializer
from . import services
from drf_spectacular.utils import extend_schema, OpenApiResponse


class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")
        last_name = self.request.query_params.get("last_name")

        if name or last_name:
            return services.get_patients_by_full_name(name=name, last_name=last_name)
        return services.get_all_patients()

    def perform_create(self, serializer):
        serializer.save()


class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientDeleteAllView(APIView):
    @extend_schema(
        responses={
            204: OpenApiResponse(description="No content")
    }
    )
        
    def delete(self, request, *args, **kwargs):
        services.delete_all_patients()
        return Response(status=status.HTTP_204_NO_CONTENT)
