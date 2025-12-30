from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone


class Course(models.Model):
    # CRITICAL: This field is named 'instructor', so in HTML we MUST use {{ course.instructor }}
    instructor = models.ForeignKey(
        User, related_name='courses_taught', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    course_image = models.ImageField(
        upload_to='course_images/', blank=True, null=True)
    image_url = models.URLField(default="https://placehold.co/600x400")
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
        User, related_name='courses_joined', blank=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(
        blank=True, null=True, help_text="Write your lesson and paste diagrams here")
    video_url = models.URLField(
        blank=True, null=True, help_text="Youtube link, etc.")
    order = models.PositiveIntegerField(default=0)
    quiz_question = models.CharField(
        max_length=300, blank=True, null=True, help_text="Enter a quiz question for this lesson")
    option_a = models.CharField(max_length=200, blank=True, null=True)
    option_b = models.CharField(max_length=200, blank=True, null=True)
    option_c = models.CharField(max_length=200, blank=True, null=True)

    CORRECT_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C')]
    correct_answer = models.CharField(
        max_length=1, choices=CORRECT_CHOICES, blank=True, null=True)
    lesson_file = models.FileField(
        upload_to='lesson_files/', blank=True, null=True, help_text="Upload PDF, PPT, or ZIP")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_video_id(self):
        if not self.video_url:
            return None
        if "v=" in self.video_url:
            return self.video_url.split("v=")[1].split("&")[0]
        elif "youtu.be" in self.video_url:
            return self.video_url.split("/")[-1]
        return None

# --- PROFILE MODEL (Fixed: Only One Definition) ---


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True,
                           help_text="Short bio about the instructor")
    profile_pic = models.ImageField(
        upload_to='profile_pics/', default='default.jpg', blank=True)
    title = models.CharField(max_length=100, blank=True,
                             help_text="e.g. Senior Chemical Engineer")

    def __str__(self):
        return f'{self.user.username} Profile'

# --- SIGNALS (Automation) ---


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class LiveSession(models.Model):
    course = models.ForeignKey(
        Course, related_name='live_sessions', on_delete=models.CASCADE)
    title = models.CharField(
        max_length=200, help_text="Topic of this live class")
    meeting_id = models.CharField(max_length=100, unique=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Auto-generate a unique meeting ID if not provided
        if not self.meeting_id:
            import uuid
            # Creates a random string like 'tch101-4821'
            self.meeting_id = f"{self.course.title[:3].replace(' ', '')}-{str(uuid.uuid4())[:8]}"
        super().save(*args, **kwargs)

    def get_join_url(self):
        # Generates the secure Jitsi link
        return f"https://meet.jit.si/{self.meeting_id}"

    def __str__(self):
        return f"Live: {self.title} ({self.course.title})"
