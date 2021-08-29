from django import forms
from django.forms import fields

from .models import BaseUser


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label='Enter Username', min_length=3, max_length=50, help_text='Required'
    )
    email = forms.EmailField(
        max_length=100, help_text='Required', error_messages={'required': 'sorry, you will need an email'}        
    )
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta: # what model is this for, when ever this form validates its gonna create BUser
        model = BaseUser
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = BaseUser.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError('Username already exists')
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if BaseUser.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another email, that one is already taken'
            )
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'repeat password'}
        )
