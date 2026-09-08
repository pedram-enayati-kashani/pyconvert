from django import forms
from ..models.EmailModel import EmailSettings


class EmailSettingsForm(forms.ModelForm):
    BOOLEAN_CHOICES = (
        (True, 'روشن'),
        (False, 'خاموش'),
    )

    use_authentication = forms.TypedChoiceField(
        choices=BOOLEAN_CHOICES,
        coerce=lambda x: x == 'True' or x is True,
        label='احراز هویت',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    use_tls = forms.TypedChoiceField(
        choices=BOOLEAN_CHOICES,
        coerce=lambda x: x == 'True' or x is True,
        label='خودکار TLS',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    use_ssl = forms.TypedChoiceField(
        choices=BOOLEAN_CHOICES,
        coerce=lambda x: x == 'True' or x is True,
        label='رمزنگاری',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    status = forms.ChoiceField(
        choices=EmailSettings.STATUS_CHOICES,
        label='وضعیت فعال / غیرفعال',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = EmailSettings
        fields = [
            'username', 'password', 'host', 'port',
            'sender_email', 'sender_name', 'charset',
            'use_authentication', 'use_tls', 'use_ssl', 'status'
        ]

        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
            'host': forms.TextInput(attrs={'class': 'form-control'}),
            'port': forms.NumberInput(attrs={'class': 'form-control'}),
            'sender_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'sender_name': forms.TextInput(attrs={'class': 'form-control'}),
            'charset': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['use_authentication'].initial = self.instance.use_authentication
            self.fields['use_tls'].initial = self.instance.use_tls
            self.fields['use_ssl'].initial = self.instance.use_ssl
            self.fields['status'].initial = self.instance.status

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.use_authentication = self.cleaned_data['use_authentication']
        instance.use_tls = self.cleaned_data['use_tls']
        instance.use_ssl = self.cleaned_data['use_ssl']
        instance.status = self.cleaned_data['status']

        if commit:
            instance.save()
            self.save_m2m()

        return instance
