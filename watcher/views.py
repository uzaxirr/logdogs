from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from generator.models import Source
from watcher.models import Events
from watcher.serializer import EventSerializer


# Create your views here.
class ListenEventView(APIView):
    """Listen for events from sources"""

    def get_source(self, source_uuid):
        """Returns a `Source` model associated with the Event"""
        try:
            return Source.objects.get(webhook_uuid=source_uuid)
        except Source.DoesNotExist:
            return None

    def post(self, request, source_uuid):
        required_source = self.get_source(source_uuid=source_uuid)
        if required_source is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.data["source"] = required_source.id
        serialized_event = EventSerializer(data=request.data)
        if serialized_event.is_valid():
            serialized_event.save()
            return Response(serialized_event.data, status=status.HTTP_201_CREATED)
        return Response(serialized_event.errors, status=status.HTTP_400_BAD_REQUEST)


class EventsView(APIView):
    """List all events, or create a new event."""

    def get(self, request, source_id):
        try:
            required_source = Source.objects.get(pk=source_id)
        except Source.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        all_events = Events.objects.filter(source=source_id)
        serialized_events = EventSerializer(all_events, many=True)
        return Response(serialized_events.data)


class EventDetailedView(APIView):
    """Retrieve and Delete on `Event` model"""

    def get_object(self, pk):
        try:
            return Events.objects.get(pk=pk)
        except Events.DoesNotExist:
            raise Http404

    def get(self, request, source_uuid, pk):
        serialized_event = EventSerializer(self.get_object(pk=pk))
        return Response(serialized_event.data)

    def delete(self, request, source_uuid, pk):
        try:
            required_event = Events.objects.get(pk=pk)
        except Events.DoesNotExist:
            raise Http404
        required_event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
