import uuid
from django import forms
from django.db import transaction
from App_panel.models import ContactUs, ContactMessage
from captcha.fields import CaptchaField, CaptchaTextInput


class ContactUsModelForm(forms.ModelForm):
    captcha = CaptchaField(
        label="کد امنیتی",
        widget=CaptchaTextInput(attrs={'class': 'form-control', 'placeholder': 'کد را وارد کنید'}),
        error_messages={
            'required': 'کد امنیتی اجباری می‌باشد',
        },
    )

    title = forms.CharField(
        label='موضوع',
        max_length=150,
        error_messages={
            'max_length': 'موضوع نباید بیشتر از 150 کاراکتر باشد',
            'required': 'موضوع اجباری می‌باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    full_name = forms.CharField(
        label='نام کامل',
        max_length=60,
        error_messages={
            'max_length': 'نام کامل نباید بیشتر از 60 کاراکتر باشد',
            'required': 'نام کامل اجباری می‌باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        label='ایمیل',
        max_length=100,
        error_messages={
            'invalid': 'لطفاً یک ایمیل معتبر وارد کنید',
            'max_length': 'ایمیل نباید بیشتر از 100 کاراکتر باشد',
            'required': 'ایمیل اجباری می‌باشد',
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: info@site.com'
        }),
    )

    message = forms.CharField(
        label='پیغام',
        error_messages={
            'required': 'پیغام اجباری می‌باشد',
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 16,
        }),
    )

    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'title']

    def save(self, commit=True):
        with transaction.atomic():
            ticket = super().save(commit=False)
            if not ticket.token:
                ticket.token = uuid.uuid4().hex

            if commit:
                ticket.save()
            message_text = self.cleaned_data.get('message')
            ContactMessage.objects.create(
                ticket=ticket,
                sender_type='user',
                message=message_text
            )

        return ticket
