from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import UserManager as DjangoUserManager

class UsersQuerySet(models.QuerySet):
    def delete(self, hard=False):
        if not hard:
            return self.update(is_deleted=True, updated_at=timezone.now())
        return super().delete()

class UsersManager(DjangoUserManager.from_queryset(UsersQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Users(AbstractUser):
    def upload_avatar_path(instance, filename):
        now = datetime.now()
        return f'avatar/{now.year}/{now.month:02d}/{now.day:02d}/{filename}'
    DISPLAY_NAME_CHOICES = [("username", "نام کاربری"),("first_last", "نام نام‌خانوادگی"),("last_first", "نام‌خانوادگی نام")]
    display_name = models.CharField(max_length=20,choices=DISPLAY_NAME_CHOICES,default="username",verbose_name="نحوه نمایش نام")
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=upload_avatar_path,verbose_name="عکس",null=True,blank=True)
    mobile = models.CharField(max_length=15,verbose_name="تلفن همراه",null=True,blank=True)
    email_active_code = models.CharField(max_length=100,null=True,verbose_name="کد فعال سازی ایمیل",blank=True)
    title_seo = models.CharField(max_length=60, null=True, verbose_name="عنوان گوگل",blank=True)
    description = models.TextField(verbose_name="توضیحات",null=True,blank=True)
    description_seo = models.TextField(verbose_name="توضیحات",null=True,blank=True)
    summery = models.TextField(verbose_name="توضیحات",null=True,blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name="حذف شده / نشده")
    created_by = models.ForeignKey("self", on_delete=models.SET_NULL,null=True,blank=True,related_name="created_users",verbose_name="ایجاد شده توسط")
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    objects = UsersManager()
    all_objects = models.Manager()

    def __str__(self):
        if self.display_name == "username":
            return self.username
        elif self.display_name == "first_last":
            return f"{self.first_name} {self.last_name}".strip()
        elif self.display_name == "last_first":
            return f"{self.last_name} {self.first_name}".strip()

    class Meta:
        verbose_name= 'کاربر'
        verbose_name_plural= 'کاربران'

    def delete(self, using=None, keep_parents=False, hard=False):
        if hard:
            return super().delete(using, keep_parents)
        self.is_deleted = True
        self.save(update_fields=['is_deleted', 'updated_at'])

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=['is_deleted', 'updated_at'])

    def toggle_status(self):
        self.is_active = not self.is_active
        self.save()