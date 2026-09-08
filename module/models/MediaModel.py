import uuid
from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models


class Media(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "فعال"),
        (STATUS_INACTIVE, "غیرفعال"),
    ]

    TYPE_IMAGE = "image"
    TYPE_VIDEO = "video"
    TYPE_MUSIC = "sound"

    MEDIA_TYPE_CHOICES = [
        (TYPE_IMAGE, "تصویر"),
        (TYPE_VIDEO, "ویدیو"),
        (TYPE_MUSIC, "صوت"),
    ]

    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )

    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
    ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".webm", ".mkv"}
    ALLOWED_MUSIC_EXTENSIONS = {".mp3", ".wav", ".ogg"}

    MAX_IMAGE_SIZE = 10 * 1024 * 1024
    MAX_VIDEO_SIZE = 100 * 1024 * 1024
    MAX_MUSIC_SIZE = 20 * 1024 * 1024

    def upload_media(instance, filename):
        extension = Path(filename).suffix.lower()

        if extension in Media.ALLOWED_IMAGE_EXTENSIONS:
            directory = "images"
        elif extension in Media.ALLOWED_VIDEO_EXTENSIONS:
            directory = "videos"
        elif extension in Media.ALLOWED_MUSIC_EXTENSIONS:
            directory = "music"
        else:
            directory = "others"

        return f"media/{directory}/{instance.media_key}{extension}"

    title = models.CharField(max_length=60, null=True, blank=True)

    media_key = models.CharField(
        max_length=32,
        unique=True,
        editable=False,
        blank=True,
    )

    media = models.FileField(
        upload_to=upload_media,
        verbose_name="فایل رسانه",
        blank=True,
        null=True,
    )

    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        editable=False,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="نوع رسانه",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        db_index=True,
        verbose_name="وضعیت",
    )
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "رسانه"
        verbose_name_plural = "رسانه‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_media_type_display()}: {self.media_key}"

    def generate_media_key(self):
        return uuid.uuid4().hex

    def detect_media_type(self):
        if not self.media:
            return None

        extension = Path(self.media.name).suffix.lower()

        if extension in self.ALLOWED_IMAGE_EXTENSIONS:
            return self.TYPE_IMAGE
        if extension in self.ALLOWED_VIDEO_EXTENSIONS:
            return self.TYPE_VIDEO
        if extension in self.ALLOWED_MUSIC_EXTENSIONS:
            return self.TYPE_MUSIC

        return None

    def get_mime_type(self):
        """
        MIME type بر اساس پسوند فایل
        """
        if not self.media:
            return None

        extension = Path(self.media.name).suffix.lower()

        video_mime_types = {
            ".mp4": "video/mp4",
            ".webm": "video/webm",
            ".mkv": "video/x-matroska",
        }

        music_mime_types = {
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".ogg": "audio/ogg",
        }

        image_mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".gif": "image/gif",
            ".avif": "image/avif",
        }

        return (
            video_mime_types.get(extension)
            or music_mime_types.get(extension)
            or image_mime_types.get(extension)
        )

    @property
    def video_mime_type(self):
        if not self.media:
            return None

        extension = Path(self.media.name).suffix.lower()
        return {
            ".mp4": "video/mp4",
            ".webm": "video/webm",
            ".mkv": "video/x-matroska",
        }.get(extension)

    @property
    def sound_mime_type(self):
        if not self.media:
            return None

        extension = Path(self.media.name).suffix.lower()
        return {
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".ogg": "audio/ogg",
        }.get(extension)

    def clean(self):
        super().clean()

        if not self.media:
            return

        detected_type = self.detect_media_type()

        if detected_type is None:
            allowed_extensions = sorted(
                self.ALLOWED_IMAGE_EXTENSIONS
                | self.ALLOWED_VIDEO_EXTENSIONS
                | self.ALLOWED_MUSIC_EXTENSIONS
            )
            raise ValidationError({
                "media": f"فرمت فایل مجاز نیست. فرمت‌های مجاز: {', '.join(allowed_extensions)}"
            })

        self.media_type = detected_type

        if detected_type == self.TYPE_IMAGE:
            max_size = self.MAX_IMAGE_SIZE
            file_label = "تصویر"
        elif detected_type == self.TYPE_VIDEO:
            max_size = self.MAX_VIDEO_SIZE
            file_label = "ویدیو"
        else:
            max_size = self.MAX_MUSIC_SIZE
            file_label = "صوت"

        if self.media.size > max_size:
            max_size_mb = max_size // (1024 * 1024)
            raise ValidationError({
                "media": f"حجم {file_label} نباید بیشتر از {max_size_mb} مگابایت باشد."
            })

    def save(self, *args, **kwargs):
        if not self.media_key:
            self.media_key = self.generate_media_key()

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def ckeditor_tag(self):
        return f"[{self.media_type}:{self.media_key}]"

    @property
    def is_image(self):
        return self.media_type == self.TYPE_IMAGE

    @property
    def is_video(self):
        return self.media_type == self.TYPE_VIDEO

    @property
    def is_music(self):
        return self.media_type == self.TYPE_MUSIC

    def toggle_status(self):
        self.status = (
            self.STATUS_INACTIVE if self.status == self.STATUS_ACTIVE else self.STATUS_ACTIVE
        )
        self.save(update_fields=["status"])
