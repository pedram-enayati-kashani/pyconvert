from django.db import models
from App_panel.models.SectionModel import Section

class AdvText(models.Model):
    STATUS_CHOICES = [('active', 'فعال'), ('inactive', 'غیرفعال')]
    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )
    title = models.CharField(max_length=200)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, related_name="section_adv_text", verbose_name="بخش نمایش",null=True, blank=True)
    url = models.URLField(verbose_name="آدرس",default='address')
    address_list = models.CharField(max_length=50, verbose_name="لیست آدرس", null=True, blank=True)
    click_count = models.IntegerField(verbose_name="تعداد کلیک", default=0,null=True, blank=True)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    rel = models.CharField(max_length=100, default='')
    target_blank = models.BooleanField(default=False, verbose_name="باز شدن در تب جدید")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
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

class AdvImage(models.Model):
    def upload_image_Adv(instance, filename):
        return f'adv_image/{filename}'

    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )
    STATUS_CHOICES = [('active', 'فعال'), ('inactive', 'غیرفعال')]
    title = models.CharField(max_length=200)
    image = models.ImageField(max_length=200,upload_to=upload_image_Adv, verbose_name="عکس")
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, related_name="section_adv_image", verbose_name="بخش نمایش",null=True, blank=True)
    url = models.URLField(verbose_name="آدرس",default='address')
    address_list = models.CharField(max_length=50, verbose_name="لیست آدرس", null=True, blank=True)
    click_count = models.IntegerField(verbose_name="تعداد کلیک", default=0,null=True, blank=True)
    rel = models.CharField(max_length=100, default='')
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True)
    target_blank = models.BooleanField(default=False, verbose_name="باز شدن در تب جدید")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
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