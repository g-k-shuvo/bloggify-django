from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from .models import Profile

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs={'class': 'form-control'}
        self.fields['password2'].widget.attrs={'class': 'form-control'}
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
                'username': forms.TextInput(attrs={
                    'class': "form-control"
                    }),
                'email': forms.EmailInput(attrs={
                    'class': "form-control"
                    })
            }

class UserUpdateForm(forms.ModelForm):
    class Meta:
            model = User
            fields = ['first_name', 'last_name', 'email']
            widgets = {
                'first_name': forms.TextInput(attrs={
                    'class': 'form-control'
                }),
                'last_name': forms.TextInput(attrs={
                    'class': 'form-control'
                })
            }

class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs={'class': 'form-control'}
    class Meta:
        model = Profile
        fields = ['bio', 'work', 'address', 'profile_pic']
        widgets = {
                'bio': forms.Textarea(attrs={
                    'class': "form-control",
                    'rows': 3
                }),
                'work': forms.Textarea(attrs={
                    'class': "form-control",
                    'rows': 3
                }),
                'address': forms.Textarea(attrs={
                    'class': "form-control",
                    'rows': 3
                ,})
            }
