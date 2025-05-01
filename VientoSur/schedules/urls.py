from django.urls import path
from . import views

urlpatterns = [
    path(
        "schedules/",
        views.RecurringScheduleListCreateView.as_view(),
        name="recurring-schedule-list-create",
    ),
    path(
        "schedules/<int:pk>/",
        views.RecurringScheduleRetrieveUpdateDestroyView.as_view(),
        name="recurring-schedule-retrieve-update-destroy",
    ),
    path(
        "schedules/delete_all/",
        views.RecurringScheduleDeleteAllView.as_view(),
        name="recurring-schedule-delete-all",
    ),
]
