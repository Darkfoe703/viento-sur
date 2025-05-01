from django.urls import path
from . import views

urlpatterns = [
    path(
        "appointments/",
        views.AppointmentListCreateView.as_view(),
        name="appointment-list-create",
    ),
    path(
        "appointments/<int:pk>/",
        views.AppointmentRetrieveUpdateDestroyView.as_view(),
        name="appointment-retrieve-update-destroy",
    ),
    path(
        "appointments/delete_all", views.AppointmentDeleteAllView.as_view(),
        name="appointment-delete-all",
    ),
]
