from django import forms
from App_panel.models.SMSModel import SMSSettings
from django.utils import translation


class SmsSettingsForm(forms.ModelForm):
    username = forms.CharField(
        label='نام کاربری',
        error_messages={
            'required': 'نام کاربری اجباری می‌باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label='کلمه عبور',
        error_messages={
            'required': 'کلمه عبور اجباری می‌باشد',
        },
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    body_id = forms.CharField(
        label='شناسه الگو',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    status = forms.TypedChoiceField(
        choices=[
            ('active', 'فعال'),
            ('inactive', 'غیرفعال')
        ],
        coerce=str,
        initial='active',
        label='وضعیت',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = SMSSettings
        fields = [
            'username', 'password', 'body_id', 'status'
        ]

    def __init__(self, *args, user=None, request=None, **kwargs):
        self.request = request

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.lang = self.lang

        if commit:
            instance.save()
            self.save_m2m()

        return instance
