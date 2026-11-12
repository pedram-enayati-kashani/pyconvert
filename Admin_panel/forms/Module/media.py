import uuid
from pathlib import Path
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from module.models.MediaModel import Media

class MediaForm(forms.ModelForm):
    title = forms.CharField(
        label=_('Title'),
        max_length=60,
        error_messages={
            'required': _("Title is required."),
            'max_length': _("Title cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    media = forms.FileField(
        label=_('Media file (Image, Video or Audio)'),
        error_messages={
            'required': _("Media file selection is required."),
        },
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/*,video/*,audio/*',
            }
        ),
    )

    status = forms.TypedChoiceField(
        choices=[
            ('active', _("Active")),
            ('inactive', _("Inactive")),
        ],
        coerce=str,
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Media
        fields = [
            'title',
            'media',
            'status',
        ]

    def __init__(self, *args, request=None, **kwargs):

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        self.request = request

        super().__init__(*args, **kwargs)

    def clean_media(self):
        """اعتبارسنجی فایل آپلود شده"""
        media_file = self.cleaned_data.get('media')

        if not media_file:
            return media_file

        ext = Path(media_file.name).suffix.lower().lstrip('.')

        allowed_images = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
        allowed_videos = {'mp4', 'mov', 'avi', 'mkv', 'webm'}
        allowed_audios = {'mp3', 'wav', 'ogg', 'm4a', 'aac'}

        if ext in allowed_images:
            self.cleaned_data['media_type'] = 'image'
        elif ext in allowed_videos:
            self.cleaned_data['media_type'] = 'video'
        elif ext in allowed_audios:
            self.cleaned_data['media_type'] = 'audio'
        else:
            raise ValidationError(
                _('File format not allowed. Only image, video, or audio are allowed.')
            )

        max_size = 100 * 1024 * 1024  # 100 MB
        if media_file.size > max_size:
            raise ValidationError(
                _('File size cannot exceed 100 MB.')
            )

        return media_file

    def save(self, commit=True):
        """ذخیره اطلاعات در دیتابیس"""
        instance = super().save(commit=False)

        media_type = self.cleaned_data.get('media_type')
        instance.media_type = media_type
        instance.lang = self.lang
        if media_type == 'image':
            prefix = 'IMG'
        elif media_type == 'video':
            prefix = 'VID'
        else:
            prefix = 'AUD'

        instance.media_key = f'{prefix}-{uuid.uuid4().hex[:12].upper()}'

        if commit:
            instance.save()
            self.save_m2m()

        return instance