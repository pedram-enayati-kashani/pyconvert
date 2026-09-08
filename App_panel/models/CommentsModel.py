from django.db import models
from django.conf import settings
from App_panel.models.PostModel import Post

class Comments(models.Model):
    STATUS_CHOICES = (
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
        ('pending', 'در انتظار تایید'),
    )
    SAW_CHOICES = (
        ('see', 'مشاهده شده'),
        ('not-see', 'مشاهده نشده'),
    )
    LANG_CHOICES = (
        ('fa', 'قارسی'),
        ('en', 'انگلیسی'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name="comment_user",verbose_name="کاربر",null=True,blank=True)
    fullName = models.CharField(max_length=60, verbose_name='نام',null=True,blank=True)
    email = models.EmailField(max_length=300, verbose_name='ایمیل',null=True,blank=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,related_name="children",null=True, blank=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments",null=True, blank=True)
    body = models.TextField(verbose_name='نظر',blank=True)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa', db_index=True,null=True, blank=True)
    response = models.TextField(verbose_name='متن پاسخ', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,db_index=True, default='pending', verbose_name="تایید / رد")
    saw = models.CharField(max_length=10, choices=SAW_CHOICES, default='not-see', verbose_name="مشاهده شده / مشاهده نشده")
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return self.body