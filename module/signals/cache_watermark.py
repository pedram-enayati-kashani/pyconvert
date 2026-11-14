from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from module.models.WaterMarkModel import WaterMark
from Admin_panel.helpers.lang import getLang


@receiver([post_save, post_delete], sender=WaterMark)
def clear_cache_on_field_change(sender, instance, **kwargs):
    cache.delete(f"active_watermark_settings_{getLang()}")
