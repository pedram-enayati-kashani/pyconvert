from django.db import models
from django.contrib.auth.models import Group

class GroupExtra(models.Model):
    STATUS_CHOICES = (
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
    )
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="extra")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active',verbose_name="فعال / غیرفعال")

    def toggle_status(self):
        if self.status == 'active':
            self.status = 'inactive'
        else:
            self.status = 'active'
        self.save()