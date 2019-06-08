from django import forms

from .models import User


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'field'}), max_length=12, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'field'}), max_length=12, min_length=8)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'date_of_birth', 'password', 'confirm_password')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'field'}),
            'last_name': forms.TextInput(attrs={'class': 'field'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'field'}),
            'email': forms.EmailInput(attrs={'class': 'field'}),
        }


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'field'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'field'}), max_length=12, min_length=8)


class CompleteSignup(forms.Form):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'field'}), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'field'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'field'}))
