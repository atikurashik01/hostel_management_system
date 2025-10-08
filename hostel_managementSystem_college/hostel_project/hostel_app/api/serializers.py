from rest_framework import serializers
from hostel_app.models import Room, Student, Fee


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_number', 'capacity', 'status']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'gender', 'contact', 'room']


class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = ['id', 'student', 'month', 'amount', 'status']
