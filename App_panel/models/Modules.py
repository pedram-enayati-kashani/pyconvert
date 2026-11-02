from django.db import models
from django.core.cache import cache

class Modules(models.Model):
    name = models.CharField(max_length=60,unique=True,default='unique')
    status = models.CharField(max_length=10, default='inactive', verbose_name="فعال / غیرفعال")
    lang = models.CharField(max_length=2, default='fa', db_index=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ماژول"
        verbose_name_plural = "ماژول ها"

    def clear_status_cache(self):
        cache.delete(f"module_status_{self.name}")

    def toggle_status(self):
        self.status = 'inactive' if self.status == 'active' else 'active'
        self.save()
        self.clear_status_cache()