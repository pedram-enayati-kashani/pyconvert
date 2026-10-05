import uuid
from pathlib import Path
from django import forms
from django.core.exceptions import ValidationError
from module.models.MediaModel import Media

class MediaForm(forms.ModelForm):
    title = forms.CharField(
        label='نام کامل',
        max_length=60,
        error_messages={
            'required': 'نام کامل اجباری می‌باشد',
            'max_length': 'نام کامل نباید بیشتر از 60 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    media = forms.FileField(
        label='فایل رسانه (تصویر یا ویدیو)',
        error_messages={
            'required': 'انتخاب فایل رسانه الزامی است',
        },
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/*,video/*',
            }
        ),
    )

    status = forms.TypedChoiceField(
        choices=[
            ('active', 'فعال'),
            ('inactive', 'غیرفعال'),
        ],
        coerce=str,
        label='وضعیت',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Media
        fields = [
            'title',
            'media',
            'status',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_media(self):
        media_file = self.cleaned_data.get('media')

        if not media_file:
            return media_file

        ext = Path(media_file.name).suffix.lower().lstrip('.')

        allowed_images = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
        allowed_videos = {'mp4', 'mov', 'avi', 'mkv', 'webm'}

        if ext in allowed_images:
            self.cleaned_data['media_type'] = 'image'
        elif ext in allowed_videos:
            self.cleaned_data['media_type'] = 'video'
        else:
            raise ValidationError(
                'فرمت فایل مجاز نیست. فقط تصویر یا ویدیو مجاز است.'
            )

        max_size = 100 * 1024 * 1024  # 100 MB
        if media_file.size > max_size:
            raise ValidationError(
                'حجم فایل نباید بیشتر از ۱۰۰ مگابایت باشد.'
            )

        return media_file

    def save(self, commit=True):
        instance = super().save(commit=False)

        media_type = self.cleaned_data.get('media_type')
        instance.media_type = media_type

        prefix = 'IMG' if media_type == 'image' else 'VID'
        instance.media_key = f'{prefix}-{uuid.uuid4().hex[:12].upper()}'

        if commit:
            instance.save()
            self.save_m2m()

        return instance
