from django.db import models

class SMSSettings(models.Model):
    STATUS_CHOICES = (
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
    )
    LANG_CHOICES = (
        ('fa', 'فارسی'),
        ('en', 'انگلیسی'),
    )
    username = models.CharField(max_length=150, verbose_name="نام کاربری",blank=True, null=True)
    password = models.CharField(max_length=150, verbose_name="رمز عبور",blank=True, null=True)
    body_id = models.CharField(max_length=50, verbose_name="شناسه الگو",blank=True, null=True)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, db_index=True, default='inactive',
                              verbose_name="فعال / غیرفعال")

    class Meta:
        verbose_name = 'تنظیمات پیامک'
        verbose_name_plural = 'تنظیمات پیامک'

    def __str__(self):
        return f"{self.username} ({self.get_lang_display()})"