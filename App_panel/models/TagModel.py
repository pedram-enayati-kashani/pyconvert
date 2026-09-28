from django.db import models
from django.utils.text import slugify
from datetime import datetime
from django.urls import reverse

class Tag(models.Model):
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

    def upload_image_tags(instance, filename):
        now = datetime.now()
        return f'tags/{now.year}/{now.month:02d}/{now.day:02d}/{filename}'
    title = models.CharField(max_length=160, verbose_name="عنوان")
    title_seo = models.CharField(max_length=60, null=True, blank=True, verbose_name="عنوان گوگل")
    status = models.CharField(max_length=10,db_index=True, choices=STATUS_CHOICES, default='draft', verbose_name="فعال / غیرفعال")
    description = models.TextField(verbose_name="توضیحات",null=True, blank=True)
    description_seo = models.TextField(max_length=160, null=True, blank=True, verbose_name="توضیحات گوگل")
    slug = models.SlugField(null=False,db_index=True, verbose_name="اسلاک", max_length=255,allow_unicode=True,blank=True)
    image = models.ImageField(upload_to=upload_image_tags, verbose_name="عکس", null=True, blank=True)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"

    def save(self, *args, **kwargs):
        current_lang = self.lang if self.lang is not None else 'fa'
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1

            while Tag.objects.filter(slug=slug, lang=current_lang).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Client:tag', kwargs={'tag_slug': self.slug})