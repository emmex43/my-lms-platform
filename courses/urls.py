from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),  # Root of courses app
    path('<int:course_id>/', views.course_detail,
         name='course_detail'),
    path('<int:course_id>/lessons/<int:lesson_id>/',
         views.lesson_detail, name='lesson_detail'),
    path('signup/', views.signup, name='signup'),  # User signup page
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('create/', views.create_course, name='create_course'),
    path('<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('<int:course_id>/add-lesson/', views.add_lesson, name='add_lesson'),
]
