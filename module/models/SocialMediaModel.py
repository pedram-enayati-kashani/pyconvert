from django.db import models

class SocialMedia(models.Model):
    def upload_image_socialMedia(instance, filename):
        return f'socialMedia/{filename}'

    STATUS_CHOICES = [('active', 'فعال'), ('inactive', 'غیرفعال')]
    title = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200,null=True)
    url = models.URLField(null=True,blank=True)
    rel = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    icon = models.ImageField(upload_to=upload_image_socialMedia, verbose_name="ایکون",null=True,blank=True)
    target_blank = models.BooleanField(default=False, verbose_name="باز شدن در تب جدید")
    lang = models.CharField(max_length=2, default='fa', db_index=True,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "شبکه اجتماعی"
        verbose_name_plural = "شبکه‌های اجتماعی"
        constraints = [
            models.UniqueConstraint(
                fields=['lang', 'name'],
                name='unique_category_name_per_language'
            )
        ]

    def __str__(self):
        return f"{self.title}"

    def toggle_status(self):
        if self.status == 'active':
            self.status = 'inactive'
        else:
            self.status = 'active'
        self.save()