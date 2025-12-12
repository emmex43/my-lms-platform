from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson

# 1. View to list all courses


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

# 2. View to see a specific course


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

# 3. View to see a specific lesson


def lesson_detail(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id, course_id=course_id)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})

# 4. View for Student Signup (The missing part!)


@login_required
def lesson_detail(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id, course_id=course_id)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.students.add(request.user)  # Add the current user to the course
    return redirect('dashboard')


@login_required
def student_dashboard(request):
    # Get all courses where the logged-in user is listed in 'students'
    courses = request.user.courses_joined.all()
    return render(request, 'courses/dashboard.html', {'courses': courses})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('course_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
