from django.db import models
from generator.models import Project, Source


class Tag(models.Model):
    """Model representing a tag"""

    name = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Events(models.Model):
    """Model to hold log events"""

    PRIORITY_CHOICES = [
        ("P1", "P1"),
        ("P2", "P2"),
        ("P3", "P3"),
        ("P4", "P4"),
        ("P5", "P5"),
    ]

    LOG_LEVEL_CHOICES = [
        ("DEBUG", "DEBUG"),
        ("INFO", "INFO"),
        ("WARNING", "WARNING"),
        ("ERROR", "ERROR"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    log_data = models.JSONField()
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default="P4")
    log_level = models.CharField(
        max_length=7, choices=LOG_LEVEL_CHOICES, default="INFO"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
