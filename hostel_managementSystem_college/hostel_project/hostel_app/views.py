from django.shortcuts import render

# Create your views here.
# hostel_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_page
from .models import Student, Room, Fee
from django.http import JsonResponse
from django.core.cache import cache

@cache_page(60)  # cache homepage for 60 seconds to reduce DB load
def home(request):
    # Use counts and small recent lists to avoid loading entire tables into memory
    students_count = Student.objects.count()
    rooms_count = Room.objects.count()
    fees_count = Fee.objects.count()

    recent_students = Student.objects.select_related('room').order_by('-id')[:6]
    recent_rooms = Room.objects.order_by('-room_number')[:8]
    recent_fees = Fee.objects.select_related('student').order_by('-id')[:10]

    context = {
        'students_count': students_count,
        'rooms_count': rooms_count,
        'fees_count': fees_count,
        'recent_students': recent_students,
        'recent_rooms': recent_rooms,
        'recent_fees': recent_fees,
    }
    return render(request, 'hostel_app/home.html', context)

def add_student(request):
    if request.method=="POST":
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST.get('gender', 'Male')
        if gender not in ('Male', 'Female'):
            messages.error(request, 'Invalid gender selection. Please choose Male or Female.')
            return redirect('add_student')
        contact = request.POST['contact']
        room_id = request.POST['room']
        room = Room.objects.get(room_number=room_id)
        Student.objects.create(name=name, age=age, gender=gender, contact=contact, room=room)
        messages.success(request, 'Student added successfully')
        # Clear cache so dashboard updates quickly
        try:
            cache.clear()
        except Exception:
            pass
        return redirect('home')
    rooms = Room.objects.all()
    return render(request, 'hostel_app/add_student.html', {'rooms':rooms})

def add_room(request):
    if request.method=="POST":
        room_number = request.POST['room_number']
        capacity = request.POST['capacity']
        Room.objects.create(room_number=room_number, capacity=capacity)
        messages.success(request, 'Room created successfully')
        try:
            cache.clear()
        except Exception:
            pass
        return redirect('home')
    return render(request, 'hostel_app/add_room.html')

def add_fee(request):
    if request.method=="POST":
        student_id = request.POST['student']
        month = request.POST['month']
        amount = request.POST['amount']
        status = request.POST['status']
        student = Student.objects.get(id=student_id)
        Fee.objects.create(student=student, month=month, amount=amount, status=status)
        messages.success(request, 'Fee recorded successfully')
        try:
            cache.clear()
        except Exception:
            pass
        return redirect('home')
    students = Student.objects.all()
    return render(request, 'hostel_app/add_fee.html', {'students':students})

def delete_room(request, room_number):
    # Only allow POST for deletion
    if request.method != 'POST':
        messages.error(request, 'Invalid request method for deleting a room')
        return redirect('home')

    try:
        room = Room.objects.get(room_number=room_number)
    except Room.DoesNotExist:
        messages.error(request, 'Room not found')
        return redirect('home')

    # Prevent deleting a room which has assigned students
    assigned = Student.objects.filter(room=room).exists()
    if assigned:
        messages.error(request, 'Cannot delete room: students are assigned to it')
        return redirect('home')

    room.delete()
    messages.success(request, f'Room {room_number} deleted')
    try:
        cache.clear()
    except Exception:
        pass
    return redirect('home')


def delete_student(request, student_id):
    # Only allow POST for deletion
    if request.method != 'POST':
        messages.error(request, 'Invalid request method for deleting a student')
        return redirect('home')

    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        messages.error(request, 'Student not found')
        return redirect('home')

    student.delete()
    messages.success(request, f'Student {student.name} deleted')
    try:
        cache.clear()
    except Exception:
        pass
    return redirect('home')


@cache_page(60)
def home_data(request):
    """Return small JSON payload with recent students, rooms, and fees."""
    recent_students = list(Student.objects.select_related('room').order_by('-id')[:6].values('id','name','contact','gender','room__room_number'))
    recent_rooms = list(Room.objects.order_by('-room_number')[:8].values('room_number','capacity','status'))
    recent_fees = list(Fee.objects.select_related('student').order_by('-id')[:10].values('id','student__name','month','amount','status'))

    # Normalize keys for frontend
    for s in recent_students:
        s['room'] = s.pop('room__room_number')
    for f in recent_fees:
        f['student_name'] = f.pop('student__name')
    return JsonResponse({'recent_students': recent_students, 'recent_rooms': recent_rooms, 'recent_fees': recent_fees})
