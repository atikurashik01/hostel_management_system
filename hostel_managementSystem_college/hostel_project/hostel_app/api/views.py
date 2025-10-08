from rest_framework import viewsets, permissions
from hostel_app.models import Room, Student, Fee
from .serializers import RoomSerializer, StudentSerializer, FeeSerializer


class ReadWriteAuthenticated(permissions.BasePermission):
    """Allow read-only for unauthenticated, write for authenticated users."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('room_number')
    serializer_class = RoomSerializer
    permission_classes = [ReadWriteAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('room').all().order_by('-id')
    serializer_class = StudentSerializer
    permission_classes = [ReadWriteAuthenticated]


class FeeViewSet(viewsets.ModelViewSet):
    queryset = Fee.objects.select_related('student').all().order_by('-id')
    serializer_class = FeeSerializer
    permission_classes = [ReadWriteAuthenticated]
