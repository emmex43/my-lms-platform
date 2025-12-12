from django.contrib import admin
from .models import Course, Lesson

# This allows us to add Lessons directly inside the Course page in Admin
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)