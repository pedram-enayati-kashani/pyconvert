from django import forms
from django.core import validators
from django.utils.html import strip_tags
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from App_panel.models import Users


class UserForm(forms.ModelForm):
    username = forms.CharField(
        label= _("Username"),
        max_length=20,
        error_messages={
            'required': _("Username is required."),
            'max_length': _("Username cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        label= _("Email"),
        error_messages={
            'required': _("Email is required."),
            'invalid': _("Enter a valid email address.")
        },
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    password_con = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    is_active = forms.BooleanField(
        label=_('Is Active'),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    is_staff = forms.BooleanField(
        label=_('Admin panel access'),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(extra__status='active', extra__isnull=False),
        label=_('Group'),
        empty_label=None,
        error_messages={
            'required': _("Group selection is required."),
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'password_con','is_active','is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # check if this is a update or not
        if self.instance.pk:
            self.fields['password'].required = False
            self.fields['password_con'].required = False

            group = self.instance.groups.first()
            if group:
                self.fields['group'].initial = group.id

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            is_staff = self.cleaned_data.get('is_staff')
            new_group = self.cleaned_data.get('group')

            if is_staff and new_group:
                user.groups.set([new_group])
            else:
                user.groups.clear()

        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_con = cleaned_data.get('password_con')

        if password or password_con:
            if password != password_con:
                raise forms.ValidationError(_('Password and confirmation do not match.'))

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if self.instance and self.instance.pk and self.instance.username == username:
            return username

        if Users.all_objects.filter(username=username).exists():
            raise forms.ValidationError(_('A user with this username already exists.'))

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if self.instance and self.instance.pk and self.instance.email == email:
            return email

        if Users.all_objects.filter(email=email).exists():
            raise forms.ValidationError(_('A user with this email already exists.'))

        return email

