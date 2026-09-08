from django import forms
from django.core import validators
from django.utils.html import strip_tags
from django.contrib.auth.models import Group
from App_panel.models import Users


class UserForm(forms.ModelForm):
    username = forms.CharField(
        label='نام کاربری',
        max_length=20,
        error_messages={
            'required': 'عنوان اجباری می‌باشد',
            'max_length': 'عنوان نباید بیشتر از 20 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        label='ایمیل',
        error_messages={
            'required': 'ایمیل اجباری می‌باشد',
            'invalid': 'ایمیل معتبر وارد کنید'
        },
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    password_con = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    is_active = forms.BooleanField(
        label='فعال باشد',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    is_staff = forms.BooleanField(
        label='دسترسی به پنل ادمین',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(extra__status='active', extra__isnull=False),
        label='گروه',
        empty_label=None,
        error_messages={
            'required': 'انتخاب بخش اجباری می‌باشد',
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
                raise forms.ValidationError('رمز عبور و تکرار آن یکسان نیستند')

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.pk and self.instance.username == username:
            return username
        if Users.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('کاربری با این نام کاربری وجود دارد')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.pk and self.instance.email == email:
            return email
        if Users.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('کاربری با این ایمیل قبلاً ثبت شده است')
        return email

