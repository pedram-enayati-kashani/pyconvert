from django.db import models

class EmailSettings(models.Model):
    STATUS_CHOICES = (
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
    )
    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )
    username = models.EmailField(verbose_name='نام کاربری')
    password = models.CharField(max_length=255, verbose_name='رمز')
    host = models.CharField(max_length=255, verbose_name='سرور خروجی')
    port = models.PositiveIntegerField(default=25, verbose_name='پورت smtp')
    sender_email = models.EmailField(verbose_name='ایمیل ارسال کننده')
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    sender_name = models.CharField(max_length=255, verbose_name='نام ارسال کننده')
    charset = models.CharField(max_length=50, default='UTF-8', verbose_name='فرمت نوشتاری')
    use_authentication = models.BooleanField(default=True, verbose_name='احراز هویت')
    use_tls = models.BooleanField(default=False, verbose_name='خودکار TLS')
    use_ssl = models.BooleanField(default=False, verbose_name='رمزنگاری')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, db_index=True, default='active',
                              verbose_name="فعال / غیرفعال")

    class Meta:
        verbose_name = 'تنظیمات ایمیل'
        verbose_name_plural = 'تنظیمات ایمیل'

    def __str__(self):
        return self.host
