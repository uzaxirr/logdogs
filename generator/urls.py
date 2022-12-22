from django.urls import path

from generator.views import (
    ProjectView,
    ProjectDetailedView,
    SourceView,
    SourceDetailedView,
)
from watcher.views import EventsView

urlpatterns = [
    path("projects/", ProjectView.as_view(), name="projects"),
    path("project/<int:pk>/", ProjectDetailedView.as_view(), name="project_detail"),
    path("project/<int:project_id>/sources", SourceView.as_view(), name="sources"),
    path(
        "project/<int:project_id>/source/<int:pk>/",
        SourceDetailedView.as_view(),
        name="source_detail",
    ),
    path("source/<int:source_id>/events", EventsView.as_view(), name="list_events"),
]
