from django.urls import path

from generator.views import ProjectView, ProjectDetailView

urlpatterns = [
    path("projects/", ProjectView.as_view(), name="projects"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
]
