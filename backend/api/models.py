import uuid
from django.db import models

# Create your models here.

class AnalysisJob(models.Model):
    
    SOURCE_CHOICES = [
        ('github', 'GitHub URL'),
        ('zip', 'Upload Zip'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('complete', 'Complete'),
        ('failed', 'Failed'),
    ]

    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    source_type = models.CharField(max_length = 10, choices = SOURCE_CHOICES, default='GitHub')
    source_ref = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    graph_json = models.JSONField(null = True, blank = True)
    error = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return f"{self.job_id} - {self.status}"

    class Meta:
        ordering = ['-created_at']

