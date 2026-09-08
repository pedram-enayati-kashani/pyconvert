import os
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from App_panel.models.SectionModel import Section
from App_panel.models.CategoriesModel import Category
from App_panel.models.TagModel import Tag
from App_panel.models.PageModel import Page

class PostQuerySet(models.QuerySet):
    def delete(self, hard=False):
        if not hard:
            return self.update(is_deleted=True, updated_at=timezone.now())
        return super().delete()

class PostManager(models.Manager.from_queryset(PostQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'پیش نویس'),
        ('pending', 'در انتظار تایید'),
        ('published', 'منتشر شده'),
        ('rejected', 'رد شده'),
    )

    WATERMARK_CHOICES = (
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
    )

    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )
    def upload_image_Post_path(instance, filename):
        now = datetime.now()
        return f'posts/{now.year}/{now.month:02d}/{now.day:02d}/{filename}'

    title = models.CharField(max_length=150, verbose_name="عنوان")
    title_search = models.CharField(max_length=150, verbose_name="عنوان سرچ گوگل")
    summery = models.TextField(verbose_name="خلاصه")
    summery_search = models.TextField(verbose_name="خلاصه سرچ گوگل")
    body = models.TextField(verbose_name="محتوا")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="author",null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, related_name="section", verbose_name="بخش نمایش",null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name="categories", verbose_name="دسته بندی")
    tags = models.ManyToManyField(Tag, related_name="tags", verbose_name="برچسب", blank=True)
    pages = models.ForeignKey(Page, on_delete=models.SET_NULL, related_name="pages", verbose_name="صفحات",default=1,null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_Post_path, verbose_name="عکس")
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    status = models.CharField(max_length=10,db_index=True, choices=STATUS_CHOICES, default='active', verbose_name="فعال / غیرفعال")
    slug = models.SlugField(default='', null=False, db_index=True, max_length=255, unique=True,allow_unicode=True,blank=True)
    is_deleted = models.BooleanField(default=False, db_index=True,verbose_name="حذف شده / نشده")
    watermark = models.CharField(max_length=10, db_index=True, choices=WATERMARK_CHOICES, default='active',verbose_name="فعال / غیرفعال")
    view_numbers = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()
    all_objects = models.Manager()
    # def get_absolute_url(self):
    #     return reverse('product-detail', args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "پوست"
        verbose_name_plural = "پوست ها"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Post.all_objects.filter(slug=slug).exclude(pk=self.pk).exists():
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
        return reverse('Client:post', kwargs={'post_slug': self.slug})


class PostGallery(models.Model):

    def upload_image_Post_gallery_path(instance, filename):
        if hasattr(instance, 'post') and instance.post_id:
            post_id = instance.post_id
        else:
            post_id = 'temp'

        # ساخت مسیر: posts_gallery/{post_id}/{filename}
        return os.path.join('posts_gallery', str(post_id), filename)

    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='gallery_items',verbose_name="پست")
    image = models.ImageField(upload_to=upload_image_Post_gallery_path,verbose_name="تصویر گالری")
    created_at = models.DateTimeField(auto_now_add=True)
    alt_text = models.CharField(max_length=150,blank=True,verbose_name="متن جایگزین (سئو)")

    class Meta:
        verbose_name = "تصویر گالری"
        verbose_name_plural = "گالری تصاویر"

    def __str__(self):
        return f"تصویر برای پست: {self.post.title}"