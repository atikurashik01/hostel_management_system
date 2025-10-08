from django.db import models

# Create your models here.
# hostel_app/models.py
from django.db import models

class Room(models.Model):
    room_number = models.CharField(max_length=10, primary_key=True)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, default="Available")

    def __str__(self):
        return self.room_number

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    contact = models.CharField(max_length=15)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=(('Paid','Paid'),('Unpaid','Unpaid')), default='Unpaid')
