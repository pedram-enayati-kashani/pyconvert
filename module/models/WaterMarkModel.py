from django.db import models

class WaterMark(models.Model):
    def upload_water_mark(instance, filename):
        return f'water_mark/{filename}'

    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )

    POSITION_CHOICES = [
        ('top-left', 'بالا چپ'),
        ('top-center', 'بالا وسط'),
        ('top-right', 'بالا راست'),
        ('center-left', 'وسط چپ'),
        ('center', 'وسط'),
        ('center-right', 'وسط راست'),
        ('bottom-left', 'پایین چپ'),
        ('bottom-center', 'پایین وسط'),
        ('bottom-right', 'پایین راست'),
    ]

    SIZE_MODE_CHOICES = [('auto', 'اتوماتیک'),('manual', 'دستی'),("self-wh", "ارتفاع یا عرض خود عکس"),]
    STATUS_CHOICES = [('active', 'فعال'), ('inactive', 'غیرفعال')]
    image = models.ImageField(upload_to=upload_water_mark,verbose_name='تصویر واترمارک')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    width_mode = models.CharField(max_length=10,choices=SIZE_MODE_CHOICES,default='auto')
    height_mode = models.CharField(max_length=10,choices=SIZE_MODE_CHOICES,default='auto')
    width_percent = models.PositiveIntegerField(default=20,help_text='درصد نسبت به عرض تصویر',null=True,blank=True)
    height_percent = models.PositiveIntegerField(default=20,help_text='درصد نسبت به ارتفاع تصویر',null=True,blank=True)
    manual_width = models.PositiveIntegerField(blank=True,null=True)
    manual_height = models.PositiveIntegerField(blank=True,null=True)
    position = models.CharField(max_length=20,choices=POSITION_CHOICES,default='bottom-right')
    opacity = models.PositiveIntegerField(default=70,help_text='عدد بین 0 تا 100')
    padding = models.PositiveIntegerField(default=10,help_text='فاصله از لبه‌ها')
    version = models.PositiveIntegerField(default=1)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'تنظیم واترمارک'
        verbose_name_plural = 'تنظیمات واترمارک'

    def __str__(self):
        return f"Watermark #{self.image}"

    def save(self, *args, **kwargs):
        if self.pk:
            self.version += 1

        super().save(*args, **kwargs)
