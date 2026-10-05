from django.core.cache import cache
from module.models.WaterMarkModel import WaterMark

def get_watermark():
    cache_key = "active_watermark_settings"
    watermark_setting = cache.get(cache_key)

    if watermark_setting is None:
        watermark_setting = (
            WaterMark.objects
            .filter(status='active')
            .order_by('-id')
            .first()
        )

        cache.set(cache_key, watermark_setting, 60 * 60)

    return watermark_setting