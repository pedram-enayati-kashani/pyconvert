from django import forms
from django.core import validators

class LoginForm(forms.Form):
    username = forms.CharField(
        label='ایمیل / نام کاربری',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    remember_me = forms.BooleanField(
        label='مرا به خاطر بسپار',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
