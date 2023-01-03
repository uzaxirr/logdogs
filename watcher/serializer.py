from rest_framework import serializers

from generator.models import Source
from watcher.models import Events


class EventSerializer(serializers.Serializer):
    """
    Serializer class for 'Event' model.
    """

    id = serializers.IntegerField(label="ID", read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=100)
    source = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all())
    log_data = serializers.JSONField()
    priority = serializers.ChoiceField(choices=Events.PRIORITY_CHOICES)
    log_level = serializers.ChoiceField(choices=Events.LOG_LEVEL_CHOICES)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Event` instance, given the validated data.
        """
        return Events.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return a new `Snippet` instance, given the validated data.
        """

        instance.title = validated_data.get("name", instance.name)
        instance.description = validated_data.get(
            "description", instance.description)
        instance.source = validated_data.get("project", instance.project)
        instance.log_data = validated_data.get(
            "webhook_uuid", instance.webhook_uuid)
        instance.priority = validated_data.get("priority", instance.created_at)
        instance.log_level = validated_data.get(
            "log_level", instance.log_level)
        instance.created_at = validated_data.get(
            "created_at", instance.created_at)
        instance.updated_at = validated_data.get(
            "updated_at", instance.updated_at)
        instance.save()
        return instance
