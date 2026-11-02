import uuid
from django.db import models
from django.conf import settings
from App_panel.models.UsersModel import Users
from datetime import datetime

class ContactUs(models.Model):
    token = models.CharField(max_length=64,unique=True,default=uuid.uuid4,editable=False,verbose_name='توکن پیگیری')
    title = models.CharField(max_length=300, verbose_name='عنوان موضوع')
    email = models.EmailField(max_length=300, verbose_name='ایمیل فرستنده')
    full_name = models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')
    status = models.CharField(max_length=15, default='pending', verbose_name='وضعیت تیکت')
    lang = models.CharField(max_length=2, default='fa', db_index=True,null=True, blank=True)
    saw = models.CharField(max_length=10, default='not-see', verbose_name='وضعیت مشاهده ادمین')
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد تیکت', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    class Meta:
        verbose_name = 'تیکت تماس با ما'
        verbose_name_plural = 'تیکت‌های تماس با ما'

    def __str__(self):
        return f"{self.title} - {self.full_name}"


class ContactMessage(models.Model):
    def upload_image_contact_message(instance, filename):
        now = datetime.now()
        return f'contact/{now.year}/{now.month:02d}/{now.day:02d}/{filename}'

    SENDER_CHOICES = (
        ('user', 'کاربر (بازدیدکننده)'),
        ('admin', 'پشتیبان (ادمین)'),
    )

    ticket = models.ForeignKey(ContactUs,on_delete=models.CASCADE,related_name='messages',verbose_name='تیکت مربوطه')
    sender_type = models.CharField(max_length=10,choices=SENDER_CHOICES,default='user',verbose_name='فرستنده پیام')
    sender_user = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='پاسخ دهنده (سیستمی)')
    message = models.TextField(verbose_name='متن پیام')
    image = models.ImageField(upload_to=upload_image_contact_message, verbose_name="عکس", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال پیام')

    class Meta:
        verbose_name = 'پیام تیکت'
        verbose_name_plural = 'پیام‌های تیکت‌ها'
        ordering = ['created_at']

    def __str__(self):
        return f"پیام برای تیکت: {self.ticket.title} ({self.get_sender_type_display()})"
