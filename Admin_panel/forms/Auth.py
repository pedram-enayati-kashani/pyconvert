from django import forms
from django.core import validators
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("Email/Username"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    remember_me = forms.BooleanField(
        label=_("Remember Me"),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
