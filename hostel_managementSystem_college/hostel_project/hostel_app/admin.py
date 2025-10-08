from django.contrib import admin

# Register your models here.
# hostel_app/admin.py
from django.contrib import admin
from .models import Room, Student, Fee

admin.site.register(Room)
admin.site.register(Student)
admin.site.register(Fee)
