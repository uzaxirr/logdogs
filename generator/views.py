from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from generator.models import Project, Source
from generator.serializers import ProjectSerializer, SourceSerializer


class ProjectView(APIView):
    """
    Create amd List on `Project` model
    """

    def get(self, request):
        all_projects = Project.objects.all()
        serialized_projects = ProjectSerializer(all_projects, many=True)
        return Response(serialized_projects.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_project = ProjectSerializer(data=request.data)
        if serialized_project.is_valid():
            serialized_project.save()
            return Response(serialized_project.data, status=status.HTTP_201_CREATED)
        return Response(serialized_project.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailedView(APIView):
    """
    Get, Update and Delete on `Project` model
    """

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        required_project = self.get_object(pk=pk)
        serialized_project = ProjectSerializer(required_project)
        return Response(serialized_project.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        required_project = Project.objects.get(pk=pk)
        serialized_project = ProjectSerializer(
            required_project, data=request.data)
        if serialized_project.is_valid():
            serialized_project.save()
            return Response(serialized_project.data, status=status.HTTP_202_ACCEPTED)
        return Response(serialized_project.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        required_project = Project.objects.get(pk=pk)
        required_project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SourceView(APIView):
    """
    Create amd List on`Source` model
    """

    def get_project(self, project_id):
        """
        Returns a `Project` model associated with the Source
        """
        try:
            return Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return None

    def get(self, request, project_id):
        project = self.get_project(project_id=project_id)
        if project is None:
            return Response(
                {"error": "project not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        all_source = Source.objects.filter(project=project)
        serialized_sources = SourceSerializer(all_source, many=True)
        return Response(serialized_sources.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        request.data["project"] = project_id
        serialized_source = SourceSerializer(data=request.data)
        if serialized_source.is_valid():
            serialized_source.save()
            return Response(serialized_source.data, status=status.HTTP_201_CREATED)
        return Response(serialized_source.errors, status=status.HTTP_400_BAD_REQUEST)


class SourceDetailedView(APIView):
    """
    Retrieve, Update and Delete on `Source` model
    """

    def get_object(self, pk):
        try:
            return Source.objects.get(pk=pk)
        except Source.DoesNotExist:
            raise Http404

    def get(self, request, project_id, pk):
        serialized_source = SourceSerializer(self.get_object(pk=pk))
        return Response(serialized_source.data)

    def put(self, request, project_id, pk):
        request.data["project"] = project_id
        serialized_source = SourceSerializer(
            self.get_object(pk=pk), data=request.data)
        if serialized_source.is_valid():
            serialized_source.save()
            return Response(serialized_source.data, status=status.HTTP_202_ACCEPTED)
        return Response(serialized_source.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, pk):
        try:
            required_source = Source.objects.get(pk=pk)
        except Source.DoesNotExist:
            raise Http404
        required_source.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
