from django import forms
from .models import Task,Category
from django.contrib.auth.forms import UserCreationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title','content','conditions')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('text',)

class SignUpForms(UserCreationForm):
    class Meta:
        fields = ('username','password1','password2')
