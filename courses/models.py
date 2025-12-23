from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Course(models.Model):
    instructor = models.ForeignKey(
        User, related_name='courses_taught', on_delete=models.CASCADE)
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
    quiz_question = models.CharField(
        max_length=300, blank=True, null=True, help_text="Enter a quiz question for this lesson")
    option_a = models.CharField(max_length=200, blank=True, null=True)
    option_b = models.CharField(max_length=200, blank=True, null=True)
    option_c = models.CharField(max_length=200, blank=True, null=True)

    CORRECT_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C')]
    correct_answer = models.CharField(
        max_length=1, choices=CORRECT_CHOICES, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_video_id(self):
        if not self.video_url:
            return None
        # Handle standard URLs (youtube.com/watch?v=...)
        if "v=" in self.video_url:
            return self.video_url.split("v=")[1].split("&")[0]
        # Handle short URLs (youtu.be/...)
        elif "youtu.be" in self.video_url:
            return self.video_url.split("/")[-1]
        return None


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# When a User is saved...

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # ...create a matching Profile for them!
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
