from django import forms
from .models import Student
from .models import Marks


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'


class MarksForm(forms.ModelForm):

    class Meta:
        model = Marks
        fields = '__all__'

class StudentSignupForm(forms.ModelForm):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['name','roll_no','email','phone','semester']