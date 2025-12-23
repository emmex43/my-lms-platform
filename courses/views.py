from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CourseForm, LessonForm
from .models import Course, Lesson

# 1. View to list all courses


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

# 2. View to see a specific course


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

# 3. View to see a specific lesson (THE CORRECT VERSION)


@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, pk=course_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    # We send BOTH 'course' and 'lesson' so the back button works
    return render(request, 'courses/lesson_detail.html', {'course': course, 'lesson': lesson})

# 4. Student Signup


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

# 5. Dashboard


@login_required
def student_dashboard(request):
    # Courses I am learning
    enrolled_courses = request.user.courses_joined.all()
    # Courses I am teaching (Added this so you can see your own courses)
    teaching_courses = Course.objects.filter(instructor=request.user)

    return render(request, 'courses/dashboard.html', {
        'enrolled_courses': enrolled_courses,
        'teaching_courses': teaching_courses
    })

# 6. Enroll in a Course


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.students.add(request.user)
    return redirect('dashboard')

# 7. Create a Course (Instructor)


@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('dashboard')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})

# 8. Edit a Course


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # NEW: Allow if user is Instructor OR Superuser
    if request.user != course.instructor and not request.user.is_superuser:
        return render(request, 'courses/error.html', {'message': "You don't have permission!"})

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/create_course.html', {'form': form})


@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # NEW: Allow if user is Instructor OR Superuser
    if request.user != course.instructor and not request.user.is_superuser:
        return render(request, 'courses/error.html', {'message': "You don't have permission!"})

    if request.method == 'POST':
        course.delete()
        return redirect('dashboard')

    return render(request, 'courses/delete_confirm.html', {'course': course})

# 10. Add a Lesson


@login_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # NEW: Allow if user is Instructor OR Superuser
    if request.user != course.instructor and not request.user.is_superuser:
        return render(request, 'courses/error.html', {'message': "You don't have permission!"})

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = LessonForm()

    return render(request, 'courses/add_lesson.html', {'form': form, 'course': course})
