from django import forms
from django.core import validators
from django_ckeditor_5.widgets import CKEditor5Widget
from App_panel.models.UsersModel import Users

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label='نام',
        max_length=60,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    last_name = forms.CharField(
        label='نام خانوادگی',
        max_length=60,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    summery = forms.CharField(
        label='خلاصه شما',
        max_length=255,
        required=False,
        error_messages={
            'required': 'خلاصه شما اجباری می‌باشد',
            'max_length': 'خلاصه شما نباید بیشتر از 255 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description_seo = forms.CharField(
        label='توضیحات گوگل',
        max_length=160,
        required=False,
        error_messages={
            'max_length': 'توضیحات گوگل نباید بیشتر از 60 کاراکتر باشد',
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    description = forms.CharField(
        label='توضیحات',
        required=False,
        error_messages={
            'required': 'توضیحات اجباری می‌باشد',
        },
        widget=CKEditor5Widget(config_name='default'),
    )

    mobile = forms.CharField(
        label='شماره موبایل',
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    display_name = forms.ChoiceField(
        label='نحوه نمایش نام',
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    avatar = forms.ImageField(
        label='عکس پروفایل',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'summery', 'description_seo','description','mobile','display_name','avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.first_name and user.last_name:
            self.fields['display_name'].choices = [
                ('username', user.username),
                ('first_last', f"{user.first_name} {user.last_name}".strip()),
                ('last_first', f"{user.last_name} {user.first_name}".strip()),
            ]
        else:
            self.fields['display_name'].choices = [
                ('username', user.username),
            ]

class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(
        label='کلمه عبور قدیمی',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )