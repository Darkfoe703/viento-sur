from django.db import models

class Patient(models.Model):
    """Patient model to store patient information.
    Include principal information and extended information."""
    id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"
