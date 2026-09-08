from django.db import models

class RedirectRule(models.Model):
    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )
    STATUS_CHOICES = [('active', 'فعال'), ('inactive', 'غیرفعال')]
    old_url = models.CharField(max_length=255, unique=True)
    new_url = models.CharField(max_length=255)
    is_permanent = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.old_url} -> {self.new_url}"

    class Meta:
        verbose_name = "قانون ریدایرکت"
        verbose_name_plural = "قوانین ریدایرکت"

    def toggle_status(self):
        if self.status == 'active':
            self.status = 'inactive'
        else:
            self.status = 'active'
        self.save()
