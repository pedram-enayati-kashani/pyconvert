from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from module.models.Advertising import AdvImage, AdvText
from App_panel.models.SectionModel import Section


def invalidate_adv_banner_caches(section_slug):
    """تابع کمکی برای حذف کلیدهای کش مربوط به بنرها و متن‌ها"""
    if section_slug:
        cache_key_banners = f"adv_banners:{section_slug}"
        cache.delete(cache_key_banners)

def invalidate_adv_text_caches(section_slug):
    if section_slug:
        cache_key_text = f"adv_text:{section_slug}"
        cache.delete(cache_key_text)

# banner
@receiver(post_save, sender=AdvImage)
def adv_image_save_handler(sender, instance, **kwargs):
    """وقتی بنر جدید ساخته یا ویرایش می‌شود"""
    if instance.section:
        invalidate_adv_banner_caches(instance.section.slug)


@receiver(post_delete, sender=AdvImage)
def adv_image_delete_handler(sender, instance, **kwargs):
    """وقتی بنر حذف می‌شود"""
    if instance.section:
        invalidate_adv_banner_caches(instance.section.slug)

# text
@receiver(post_save, sender=AdvText)
def adv_text_save_handler(sender, instance, **kwargs):
    """وقتی لینک جدید ساخته یا ویرایش می‌شود"""
    if instance.section:
        invalidate_adv_text_caches(instance.section.slug)


@receiver(post_delete, sender=AdvText)
def adv_text_delete_handler(sender, instance, **kwargs):
    """وقتی لینک حذف می‌شود"""
    if instance.section:
        invalidate_adv_text_caches(instance.section.slug)

# section
@receiver(post_save, sender=Section)
def section_save_handler(sender, instance, **kwargs):
    """وقتی خودِ سکشن تغییر می‌کند (مثلاً نامش، وضعیتش و...)"""
    invalidate_adv_banner_caches(instance.slug)
    invalidate_adv_text_caches(instance.slug)
