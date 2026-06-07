from rest_framework import serializers
from .models import JobApplication, Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'content', 'created_at')
        read_only_fields = ('id', 'created_at')


class JobApplicationSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)
    notes_count = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = (
            'id', 'company_name', 'role_title', 'status',
            'applied_date', 'job_url', 'location', 'salary_range',
            'created_at', 'updated_at', 'notes_count', 'notes',
        )
        read_only_fields = ('id', 'applied_date', 'created_at', 'updated_at')

    def get_notes_count(self, obj):
        return obj.notes.count()


class JobApplicationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list view — no notes included."""
    notes_count = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = (
            'id', 'company_name', 'role_title', 'status',
            'applied_date', 'location', 'salary_range', 'notes_count',
        )

    def get_notes_count(self, obj):
        return obj.notes.count()