from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Course, Blog  # Assuming your CustomUser model is in models.py

class RegistrationForm(UserCreationForm):
    USER_TYPES = (
        ('student', 'Student'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPES, initial='student', widget=forms.HiddenInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'content', 'description', 'level', 'language', 'fees', 'certificate','category', 'photo']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'photo', 'description']


class ReviewForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    rating = forms.IntegerField(min_value=1, max_value=5)
    text = forms.CharField(widget=forms.Textarea)

