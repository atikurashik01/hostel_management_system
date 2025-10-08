from django.urls import path, include
from rest_framework import routers
from . import views
from .api.views import RoomViewSet, StudentViewSet, FeeViewSet

router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'students', StudentViewSet)
router.register(r'fees', FeeViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_room/', views.add_room, name='add_room'),
    path('delete_room/<str:room_number>/', views.delete_room, name='delete_room'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('add_fee/', views.add_fee, name='add_fee'),
    path('home_data/', views.home_data, name='home_data'),
    path('api/', include((router.urls, 'api'))),
]
