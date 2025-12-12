from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(default="https://placehold.co/600x400")
    created_at = models.DateTimeField(auto_now_add=True)

    # This is the critical line that was missing or not applied
    students = models.ManyToManyField(
        User, related_name='courses_joined', blank=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(
        help_text="Enter the lesson content or HTML here")
    video_url = models.URLField(
        blank=True, null=True, help_text="Youtube link, etc.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_video_id(self):
        if self.video_url and "v=" in self.video_url:
            return self.video_url.split("v=")[1]
        return None
