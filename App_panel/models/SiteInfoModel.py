from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class SiteInfo(models.Model):
    def upload_image_Logo_icon(instance, filename):
        return f'site/{filename}'
    STATUS_CHOICES = (
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
    )

    maintenance_CHOICES = (
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
    )

    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )

    title = models.CharField(max_length=150, verbose_name="عنوان")
    title_seo = models.CharField(max_length=150, verbose_name="عنوان سرچ گوگل")
    description_seo = models.TextField(max_length=255, verbose_name="خلاصه سرچ گوگل")
    logo = models.ImageField(upload_to=upload_image_Logo_icon, verbose_name="لوگو")
    favicon = models.ImageField(upload_to=upload_image_Logo_icon, verbose_name="ایکون")
    favicon_16 = models.ImageField(upload_to=upload_image_Logo_icon, blank=True, null=True)
    favicon_32 = models.ImageField(upload_to=upload_image_Logo_icon, blank=True, null=True)
    apple_touch_icon = models.ImageField(upload_to=upload_image_Logo_icon, blank=True, null=True)
    android_192 = models.ImageField(upload_to=upload_image_Logo_icon, blank=True, null=True)
    android_512 = models.ImageField(upload_to=upload_image_Logo_icon, blank=True, null=True)
    favicon_ico = models.FileField(upload_to=upload_image_Logo_icon, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="فعال / غیرفعال")
    headMeta = models.TextField(verbose_name="متا های درون هد",null=True,blank=True)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    footerScript = models.TextField(verbose_name="اسکریپت های درون فوتر",null=True,blank=True)
    robotsText = models.TextField(verbose_name="محتوای robots.txt",null=True,blank=True)
    maintenance = models.CharField(max_length=10, choices=maintenance_CHOICES, default='inactive', verbose_name="فعال / غیرفعال")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.favicon:
            img = Image.open(self.favicon.path).convert("RGBA")

            self._create_icon(16, "favicon_16", img)
            self._create_icon(32, "favicon_32", img)
            self._create_icon(180, "apple_touch_icon", img)
            self._create_icon(192, "android_192", img)
            self._create_icon(512, "android_512", img)

            # favicon.ico
            buffer = BytesIO()
            img.save(buffer, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])

            self.favicon_ico.save(
                "favicon.ico",
                ContentFile(buffer.getvalue()),
                save=False
            )

            super().save(update_fields=[
                "favicon_16",
                "favicon_32",
                "apple_touch_icon",
                "android_192",
                "android_512",
                "favicon_ico"
            ])

    def _create_icon(self, size, field_name, img):
        icon = img.copy().resize((size, size), Image.LANCZOS)

        if icon.mode != "RGBA":
            icon = icon.convert("RGBA")

        buffer = BytesIO()
        icon.save(buffer, format="PNG", optimize=True, compress_level=9)

        file_name = f"favicon_{size}.png"

        getattr(self, field_name).save(
            file_name,
            ContentFile(buffer.getvalue()),
            save=False
        )

    def toggle_status(self):
        if self.status == 'active':
            self.status = 'inactive'
        else:
            self.status = 'active'
        self.save()

    def toggle_maintenance(self):
        if self.maintenance == 'active':
            self.maintenance = 'inactive'
        else:
            self.maintenance = 'active'
        self.save()