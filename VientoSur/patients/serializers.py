from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        # TODO: puedo especificar los campos individualmente:
        # fields = ('id', 'name', 'last_name', 'birth_date', 'email', 'phone_number', 'created_at')
        # read_only_fields = (
        #     "created_at",
        # )  # para que no se pueda modificar al crear/actualizar
