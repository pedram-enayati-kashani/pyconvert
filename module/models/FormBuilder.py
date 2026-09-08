from django.db import models
from django.core.exceptions import ValidationError
from App_panel.models.PostModel import Post
from django.utils import timezone

class FormQuerySet(models.QuerySet):
    def delete(self, hard=False):
        if not hard:
            return self.update(is_deleted=True, updated_at=timezone.now())
        return super().delete()

class FormManager(models.Manager.from_queryset(FormQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Form(models.Model):
    STATUS_CHOICES = [('active', 'فعال'), ('inactive', 'غیرفعال')]
    POST_TYPE_CHOICES = [('post', 'نوشته'), ('contact', 'تماس باما'), ('general', 'عمومی')]
    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )
    title = models.CharField(max_length=200)
    target_post_type = models.CharField(
        max_length=50,
        choices=POST_TYPE_CHOICES,
        verbose_name="مخصوص نوع نوشته",
        default='post'
    )
    status = models.CharField(max_length=10, db_index=True,choices=STATUS_CHOICES, default='active')
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name="حذف شده / نشده")
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FormManager()
    all_objects = models.Manager()

    def __str__(self):
        return f"{self.title} ({self.get_target_post_type_display()})"

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


class PostFormAssignment(models.Model):
    """
    Modular Interface Table: One-to-Many Form-to-Post Relationship
✅ Without any changes to the Post model
✅ Each post can only have one form
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='form_assignments',
        verbose_name="نوشته"
    )
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='assigned_posts',
        verbose_name="فرم"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post'], name='unique_post_form_assignment')
        ]
        verbose_name = "تخصیص فرم به نوشته"
        verbose_name_plural = "تخصیص فرم‌ها"

    def clean(self):
        if hasattr(self.post, 'post_type') and self.form.target_post_type:
            if self.post.post_type != self.form.target_post_type:
                raise ValidationError({
                    'form': f"فرم انتخابی مخصوص نوع «{self.form.get_target_post_type_display()}» است."
                })

    def __str__(self):
        return f"پست #{self.post.pk} → {self.form.title}"


class FormField(models.Model):
    FIELD_TYPES = (
        ("text", "متن کوتاه"), ("textarea", "متن بلند"), ("number", "عدد"),
        ("email", "ایمیل"), ("checkbox", "چک‌باکس"), ("select", "لیست کشویی"), ("radio", "دکمه رادیویی"),
    )
    STATUS_CHOICES = [('active', 'فعال'), ('inactive', 'غیرفعال')]
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="fields")
    status = models.CharField(max_length=10, db_index=True,choices=STATUS_CHOICES, default='active')
    label = models.CharField(max_length=200)
    name = models.CharField(max_length=60, unique=True,default="unique")
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
    order = models.PositiveIntegerField(default=1, verbose_name="ترتیب نمایش")
    required = models.BooleanField(default=False)
    options = models.JSONField(default=list, blank=True, help_text="برای select/radio/checkbox")
    prefix = models.CharField(max_length=50, blank=True, null=True, verbose_name="پیشوند")
    suffix = models.CharField(max_length=50, blank=True, null=True, verbose_name="پسوند")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.pk and self.order == 1:
            last_order = FormField.objects.filter(form=self.form).order_by('-order').first()
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



class FieldValue(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='custom_field_values',
        null=True,      # موقت
        blank=True,     # موقت
    )

    field = models.ForeignKey(
        FormField,
        on_delete=models.CASCADE,
        related_name='post_values',
    )

    value = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'field'],
                name='unique_custom_field_per_post',
            )
        ]
