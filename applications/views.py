from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import JobApplication, Note
from .serializers import (
    JobApplicationSerializer,
    JobApplicationListSerializer,
    NoteSerializer,
)
from .filters import JobApplicationFilter


class JobApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobApplicationFilter

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return JobApplicationListSerializer
        return JobApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this application.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this application.")
        instance.delete()


@extend_schema(parameters=[
    OpenApiParameter('application_id', OpenApiTypes.UUID, OpenApiParameter.PATH)
])
class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_application(self):
        try:
            app = JobApplication.objects.get(
                id=self.kwargs['application_id'],
                user=self.request.user
            )
            return app
        except JobApplication.DoesNotExist:
            raise PermissionDenied("Application not found or access denied.")

    def get_queryset(self):
        return Note.objects.filter(application=self.get_application())

    def perform_create(self, serializer):
        serializer.save(application=self.get_application())


@extend_schema(parameters=[
    OpenApiParameter('application_id', OpenApiTypes.UUID, OpenApiParameter.PATH),
    OpenApiParameter('note_id', OpenApiTypes.UUID, OpenApiParameter.PATH),
])
class NoteDeleteView(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(
            application__user=self.request.user,
            application__id=self.kwargs['application_id']
        )

    def get_object(self):
        try:
            return self.get_queryset().get(id=self.kwargs['note_id'])
        except Note.DoesNotExist:
            raise PermissionDenied("Note not found or access denied.")