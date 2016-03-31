from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from tbc.models import *


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['about'].label = "About Yourself"
        self.fields['insti_org'].label = "Institute/Organizaiton"
        self.fields['dept_desg'].label = "Department/Branch/Designation"
        self.fields['phone_no'].label = "Mobile No"
        self.fields['about_proj'].label = "How did you come to know about the project"
    class Meta:
        model = Profile
        exclude = ('user')
        widgets = {
        'about':forms.TextInput(attrs={'placeholder':'Tell us about yourself'}),
        'dob':forms.TextInput(attrs={'placeholder':'mm/dd/yyyy'}),
        'insti_org':forms.TextInput(attrs={'placeholder':'Name of University/Organizaiton(if corporate)'}),
        'dept_desg':forms.TextInput(attrs={'placeholder':'Name of the Department/Branch or your designation'}),
        'phone_no':forms.TextInput(attrs={'placeholder':'Phone Number Please'}),
        }
        
        
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password1', 'password2')
        

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Username'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Password'}), label='')


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'New Password'}), label='')
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Confirm New Password'}), label='')
                               


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['publisher_place'].label = "Publisher with Place"
        self.fields['isbn'].label = "ISBN No."
        self.fields['edition'].label = "Book Edition"
        self.fields['year_of_pub'].label = "Year of Publication"
        self.fields['no_chapters'].label = "Number of Chapters"
    class Meta:
        model = Book
        exclude = ('contributor', 'approved', 'reviewer', 'tags')
        widgets = {
        'title':forms.TextInput(attrs={'placeholder':'Title of the Book'}),
        'author':forms.TextInput(attrs={'placeholder':'Author of the Book'}),
        'publisher_place':forms.TextInput(attrs={'placeholder':'Name of the Publisher with Place'}),
        'isbn':forms.TextInput(attrs={'placeholder':'Valid ISBN no. of the Book'}),
        'edition':forms.TextInput(attrs={'placeholder':'Edition of the Book'}),
        'year_of_pub':forms.TextInput(attrs={'placeholder':'Year when the Book was published'}),
        'no_chapters':forms.TextInput(attrs={'placeholder':'Total number of chapters in the Book (only include chapters that have solved examples)'}),
        }
