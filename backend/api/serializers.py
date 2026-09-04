from rest_framework import serializers
from .models import AnalysisJob

class AnalysisJobSerializer(serializers.ModelSerializer):
    """
    Full serializer — used when returning job data to the frontend.
    Covers the GET /api/jobs/{id}/ and GET /api/jobs/ endpoints.
    """
    class Meta:
        model = AnalysisJob
        fields = [
            'job_id',
            'source_type',
            'source_ref',
            'status',
            'graph_json',
            'error',
            'created_at',
            'completed_at'
        ]
    
class AnalysisJobCreateSerializer(serializers.Serializer):
    """
    Input-only serializer — validates the POST /api/analyze/ request.
    Accepts either a GitHub URL or a zip file upload.
    """
    source_type = serializers.ChoiceField(choices=['github', 'zip'])
    url = serializers.CharField(required=False, allow_blank = True)
    file = serializers.FileField(required=False)

    def validate(self, data):
        if data.get('source_type') == 'github' and not data.get('url'):
            raise serializers.ValidationError(
                "URL is required when source type is GitHub."
            )
        elif data.get('source_type') == 'zip' and not data.get('file'):
            raise serializers.ValidationError(
                "A zip file is required when source type is Zip."
            )
        return data