from django import forms
from django.utils.html import strip_tags
from django_ckeditor_5.widgets import CKEditor5Widget
from App_panel.models.ContactUsModel import ContactMessage


class ContactForm(forms.ModelForm):
    message = forms.CharField(
        label='پیغام',
        error_messages={
            'required': 'پیغام اجباری می‌باشد',
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    image = forms.ImageField(
        label='عکس',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ContactMessage
        fields = ['message','image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.ticket = kwargs.pop('ticket', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.ticket = self.ticket
        obj.sender_type = 'admin'
        obj.sender_user = self.user

        if commit:
            obj.save()
        return obj
