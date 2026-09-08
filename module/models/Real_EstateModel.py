from django.db import models

class Rent(models.Model):
    TYPE_CHOICES = [('tenant', 'مستأجر'), ('lessor', 'اجاره دهنده')]
    DIRECTION_CHOICES = [
        ("", "انتخاب کنید"), ("north", "شمالی"), ("south", "جنوبی"),
        ("east", "شرقی"), ("west", "غربی"), ("east_west", "شرقی غربی"),
        ("north_east", "شمال شرقی"), ("north_west", "شمال غربی"),
        ("south_east", "جنوب شرقی"), ("south_west", "جنوب غربی"),
        ("north_south", "شمالی جنوبی"), ("two_sided", "دو نبش / دو بر"),
        ("three_sided", "سه نبش / سه بر"),
    ]
    STATUS_CHOICES = (('completed', 'پایان یافته'), ('in_progress', 'در حال پیگیری'),)
    SAW_CHOICES = (('see', 'مشاهده شده'), ('not-see', 'مشاهده نشده'),)
    DISCHARGE_CHOICES = [
        ("", "انتخاب کنید"), ("unloading", "در حال تخلیه"), ("discharge", "تخلیه شده"),
    ]
    TYPE_UNIT_CHOICES = [
        ("", "انتخاب کنید"), ("residential", "مسکونی"), ("administrative", "اداری"),
        ("commercial", "تجاری")
    ]
    fullname = models.CharField(max_length=100, verbose_name="نام کامل")
    mobile = models.CharField(max_length=15, verbose_name="تلفن همراه")
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, default='tenant', db_index=True)
    description = models.TextField(verbose_name="توضیحات", blank=True, null=True)
    room_number = models.IntegerField(default=1)
    floor = models.IntegerField(default=0)
    floor_area = models.IntegerField(default=0, verbose_name="متراژ")
    has_change = models.BooleanField(default=False)
    price = models.CharField(default=0)
    max_price = models.CharField(default=0, null=True, blank=True)
    price_month = models.CharField(default=0, null=True, blank=True)
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES, null=True, blank=True, db_index=True, verbose_name="جهت")
    address = models.TextField(verbose_name="آدرس", db_index=True)
    discharge_unit = models.CharField(max_length=20, choices=DISCHARGE_CHOICES, null=True, blank=True, db_index=True,
                                      verbose_name="واحد تخلیه")
    type_unit = models.CharField(max_length=20, choices=TYPE_UNIT_CHOICES, null=True, blank=True, db_index=True,
                                      verbose_name="واحد تخلیه")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='in_progress')
    saw = models.CharField(max_length=10, choices=SAW_CHOICES, default='not-see', verbose_name="مشاهده وضعیت")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address

    def toggle_status(self):
        if self.status == 'completed':
            self.status = 'in_progress'
        else:
            self.status = 'completed'
        self.save()

class SellBuy(models.Model):
    TYPE_CHOICES = [('buyer', 'خریدار'), ('seller', 'فروشنده')]
    DIRECTION_CHOICES = [
        ("", "انتخاب کنید"), ("north", "شمالی"), ("south", "جنوبی"),
        ("east", "شرقی"), ("west", "غربی"), ("east_west", "شرقی غربی"),
        ("north_east", "شمال شرقی"), ("north_west", "شمال غربی"),
        ("south_east", "جنوب شرقی"), ("south_west", "جنوب غربی"),
        ("north_south", "شمالی جنوبی"), ("two_sided", "دو نبش / دو بر"),
        ("three_sided", "سه نبش / سه بر"),
    ]
    STATUS_CHOICES = (('completed', 'پایان یافته'), ('in_progress', 'در حال پیگیری'),)
    SAW_CHOICES = (('see', 'مشاهده شده'), ('not-see', 'مشاهده نشده'),)
    DISCHARGE_CHOICES = [
        ("", "انتخاب کنید"), ("unloading", "در حال تخلیه"), ("discharge", "تخلیه شده"),
    ]
    TYPE_UNIT_CHOICES = [
        ("", "انتخاب کنید"), ("residential", "مسکونی"), ("administrative", "اداری"),
        ("commercial", "تجاری")
    ]
    fullname = models.CharField(max_length=100, verbose_name="نام کامل")
    mobile = models.CharField(max_length=15, verbose_name="تلفن همراه")
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, default='seller', db_index=True)
    description = models.TextField(verbose_name="توضیحات")
    room_number = models.IntegerField(default=1)
    floor = models.IntegerField(default=0, null=True, blank=True)
    floor_area = models.IntegerField(default=0, verbose_name="متراژ")
    price = models.CharField(default=0)
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES, null=True, blank=True, db_index=True, verbose_name="جهت")
    address = models.TextField(verbose_name="آدرس", null=True, blank=True, db_index=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='in_progress')
    saw = models.CharField(max_length=10, choices=SAW_CHOICES, default='not-see', verbose_name="مشاهده وضعیت")
    discharge_unit = models.CharField(max_length=20, choices=DISCHARGE_CHOICES, null=True, blank=True, db_index=True, verbose_name="واحد تخلیه")
    type_unit = models.CharField(max_length=20, choices=TYPE_UNIT_CHOICES, null=True, blank=True, db_index=True,
                                 verbose_name="واحد تخلیه")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address

    def toggle_status(self):
        if self.status == 'completed':
            self.status = 'in_progress'
        else:
            self.status = 'completed'
        self.save()

