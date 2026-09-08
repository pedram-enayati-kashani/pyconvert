from django.db import models
from django.utils import timezone

class Menu(models.Model):
    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )
    STATUS_CHOICES = [('active', 'فعال'), ('inactive', 'غیرفعال')]
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=60, unique=True, default="unique")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    link_updated_at = models.DateTimeField(default=timezone.now, db_index=True)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def toggle_status(self):
        if self.status == 'active':
            self.status = 'inactive'
        else:
            self.status = 'active'
        self.save()

class Menu_Links(models.Model):
    STATUS_CHOICES = [('active', 'فعال'), ('inactive', 'غیرفعال')]
    title = models.CharField(max_length=60, null=True)
    name = models.CharField(max_length=60, unique=True, default="unique")
    url = models.TextField(null=True,blank=True)
    address_list = models.CharField(max_length=50,verbose_name="هدف",null=True,blank=True)
    order = models.PositiveIntegerField(default=1, verbose_name="ترتیب نمایش")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name="children", null=True, blank=True,verbose_name="فرزند لینک")
    rel = models.CharField(max_length=100, default='')
    target_blank = models.BooleanField(default=False, verbose_name="باز شدن در تب جدید")
    status = models.CharField(max_length=10,db_index=True, choices=STATUS_CHOICES, default='active')
    Menu = models.ForeignKey(Menu, on_delete=models.CASCADE,related_name='menu_links')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.pk and self.order == 1:
            last_order = Menu_Links.objects.filter(Menu=self.Menu).order_by('-order').first()
            if last_order:
                self.order = last_order.order + 1
            else:
                self.order = 1

        super().save(*args, **kwargs)

    def toggle_status(self):
        if self.status == 'active':
            self.status = 'inactive'
        else:
            self.status = 'active'
        self.save()