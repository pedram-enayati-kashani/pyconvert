from django.db import models
from django.utils.text import slugify
from datetime import datetime
from django.utils import timezone
from django.urls import reverse

class SectionQuerySet(models.QuerySet):
    def delete(self, hard=False):
        if not hard:
            return self.update(is_deleted=True, updated_at=timezone.now())
        return super().delete()


class SectionManager(models.Manager.from_queryset(SectionQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Section(models.Model):
    STATUS_CHOICES = (
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
    )

    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )

    TYPE_CHOICES = (
        ('post', 'نوشته'),
        ('last_news', 'آخرین اخبار'),
        ('most_visited', 'پربازدید ترین'),
        ('most_commented', 'پربحث ترین'),
        ('adv_text', 'تبلیغ متنی'),
        ('adv_image', 'تبلیغ بنر'),
        ('no_post', 'اطلاعیه بدون نوشته'),
    )

    def upload_image_sections(instance, filename):
        now = datetime.now()
        return f'sections/{now.year}/{now.month:02d}/{now.day:02d}/{filename}'

    name = models.CharField(max_length=60, verbose_name="نام بخش",blank=True, null=True)
    title = models.CharField(max_length=60, verbose_name="عنوان")
    title_seo = models.CharField(max_length=60, null=True, verbose_name="عنوان گوگل", blank=True)
    status = models.CharField(max_length=10,db_index=True, choices=STATUS_CHOICES, default='active', verbose_name="فعال / غیرفعال")
    type = models.CharField(max_length=14, choices=TYPE_CHOICES,db_index=True, default='post', verbose_name="نوع بخش")
    description = models.TextField(max_length=255, verbose_name="توضیحات",null=True, blank=True)
    display_number = models.IntegerField(verbose_name="تعداد نمایش", default=1)
    description_seo = models.TextField(max_length=255, null=True, verbose_name="توضیحات گوگل", blank=True)
    slug = models.SlugField(default='',db_index=True, verbose_name="اسلاگ", max_length=255, unique=True,allow_unicode=True,blank=True)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_sections, verbose_name="عکس", null=True, blank=True)
    is_deleted = models.BooleanField(default=False,db_index=True, verbose_name="حذف شده / نشده")
    posts_updated_at = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SectionManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "بخش"
        verbose_name_plural = "بخش ها"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Section.all_objects.filter(slug=slug).exclude(pk=self.pk).exists():
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
        return reverse('Client:section', kwargs={'section_slug': self.slug})