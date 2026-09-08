from django.db import models
from django.utils.text import slugify
from datetime import datetime
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone
from django.urls import reverse

class PageQuerySet(models.QuerySet):
    def delete(self, hard=False):
        if not hard:
            return self.update(is_deleted=True, updated_at=timezone.now())
        return super().delete()

class PageManager(models.Manager.from_queryset(PageQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Page(models.Model):
    STATUS_CHOICES = (
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
    )
    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )
    def upload_image_pages(instance, filename):
        now = datetime.now()
        return f'pages/{now.year}/{now.month:02d}/{now.day:02d}/{filename}'

    title = models.CharField(max_length=150, verbose_name="عنوان")
    body = CKEditor5Field(verbose_name="محتوا")
    title_seo = models.CharField(max_length=60, null=True, verbose_name="عنوان گوگل", blank=True)
    description_seo = models.TextField(max_length=255, null=True, verbose_name="توضیحات گوگل", blank=True)
    slug = models.SlugField(default='', null=False, db_index=True, verbose_name="اسلاگ", max_length=255, unique=True,allow_unicode=True,blank=True)
    image = models.ImageField(upload_to=upload_image_pages, verbose_name="عکس", null=True, blank=True)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,db_index=True, default='active', verbose_name="فعال / غیرفعال")
    is_deleted = models.BooleanField(default=False,db_index=True, verbose_name="حذف شده / نشده")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PageManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "صفحه"
        verbose_name_plural = "صفحه ها"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Page.all_objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, hard=False):
        if hard:
            return super().delete(using, keep_parents)
        self.is_deleted = True
        self.save(update_fields=['is_deleted', 'updated_at'])

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=['is_deleted', 'updated_at'])

    def toggle_status(self):
        if self.status == 'active':
            self.status = 'inactive'
        else:
            self.status = 'active'
        self.save()

    def get_absolute_url(self):
        return reverse('Client:page', kwargs={'page_slug': self.slug})