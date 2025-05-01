from django.urls import path
from . import views

urlpatterns = [
    path(
        "patients/", views.PatientListCreateView.as_view(), name="patient-list-create"
    ),
    path(
        "patients/<int:pk>/",
        views.PatientRetrieveUpdateDestroyView.as_view(),
        name="patient-retrieve-update-destroy",
    ),
    path(
        "patients/delete_all/", views.PatientDeleteAllView.as_view(),
        name="patient-delete-all",
    ),
]
