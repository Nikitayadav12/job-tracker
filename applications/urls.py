from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, NoteListCreateView, NoteDeleteView

router = DefaultRouter()
router.register(r'', JobApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:application_id>/notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('<uuid:application_id>/notes/<uuid:note_id>/', NoteDeleteView.as_view(), name='note-delete'),
]