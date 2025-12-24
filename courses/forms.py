from .models import Course, Lesson, Profile  # <-- Add Profile to imports
from django import forms
from .models import Course, Lesson, Profile


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image_url', 'course_image']
        # We add the CSS classes here instead of in the HTML!
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What will students learn?'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'order', 'lesson_file', 'quiz_question',
                  'option_a', 'option_b', 'option_c', 'correct_answer']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'quiz_question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., What does HTML stand for?'}),
            'option_a': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option A'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option B'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option C'}),
            'correct_answer': forms.Select(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
