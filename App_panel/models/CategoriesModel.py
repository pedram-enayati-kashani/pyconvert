import datetime
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.utils.text import slugify

class CategoryQuerySet(models.QuerySet):
    def delete(self, hard=False):
        if not hard:
            return self.update(is_deleted=True, updated_at=timezone.now())
        return super().delete()

class CategoryManager(models.Manager.from_queryset(CategoryQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Category(models.Model):
    STATUS_CHOICES = (
        ('draft', 'پیش نویس'),
        ('pending', 'در انتظار تایید'),
        ('published', 'منتشر شده'),
        ('rejected', 'رد شده'),
    )
    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )

    def upload_image_categories(instance, filename):
        now = datetime.now()
        return f'categories/{now.year}/{now.month:02d}/{now.day:02d}/{filename}'

    title = models.CharField(max_length=255,verbose_name="عنوان")
    title_seo = models.CharField(max_length=60, null=True, verbose_name="عنوان گوگل",blank=True)
    description = models.TextField(verbose_name="توضیحات",blank=True,null=True)
    description_seo = models.TextField(max_length=160,null=True, verbose_name="توضیحات گوگل",blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active',verbose_name="فعال / غیرفعال",db_index=True)
    slug = models.SlugField(default='',verbose_name="اسلاگ",max_length=255,allow_unicode=True,db_index=True,blank=True)
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,related_name="children",null=True, blank=True,verbose_name="فرزند دسته")
    image = models.ImageField(upload_to=upload_image_categories, verbose_name="عکس",null=True,blank=True)
    is_deleted = models.BooleanField(default=False,db_index=True,verbose_name="حذف شده / نشده")
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa',db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CategoryManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

        constraints = [
            models.UniqueConstraint(
                fields=['lang', 'slug'],
                name='unique_category_slug_per_language'
            )
        ]

    def save(self, *args, **kwargs):
        current_lang = self.lang if self.lang is not None else 'fa'
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1

            while Category.all_objects.filter(slug=slug, lang=current_lang).exclude(pk=self.pk).exists():
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

    def get_absolute_url(self):
        return reverse('Client:category', kwargs={'cat_slug': self.slug})