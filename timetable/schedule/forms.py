from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Enrollment, TimetableVote

class UserRegisterForm(UserCreationForm):
    is_student = forms.BooleanField(required=False)
    is_faculty = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_student', 'is_faculty']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']

class VoteForm(forms.ModelForm):
    class Meta:
        model = TimetableVote
        fields = ['change']
