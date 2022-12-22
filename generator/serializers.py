from rest_framework import serializers

from generator.models import Project, Source


class ProjectSerializer(serializers.Serializer):
    """
    Serializer class for 'Project' model.
    """

    id = serializers.IntegerField(label="ID", read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Project` instance, given the validated data.
        """
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return a new `Project` instance, given the validated data.
        """

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.created_at = validated_data.get("created_at", instance.created_at)
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)
        instance.save()
        return instance


class SourceSerializer(serializers.Serializer):
    """
    Serializer class for 'Source' model.
    """

    id = serializers.IntegerField(label="ID", read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    webhook_uuid = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Source` instance, given the validated data.
        """
        return Source.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return a new `Snippet` instance, given the validated data.
        """

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.project = validated_data.get("project", instance.project)
        instance.webhook_uuid = validated_data.get(
            "webhook_uuid", instance.webhook_uuid
        )
        instance.created_at = validated_data.get("created_at", instance.created_at)
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)
        instance.save()
        return instance
