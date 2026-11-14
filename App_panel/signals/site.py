from django.db.models.signals import post_save, post_delete, m2m_changed
from django.core.cache import cache
from django.dispatch import receiver
from Admin_panel.helpers.lang import getLang
from App_panel.models.SiteInfoModel import SiteInfo

@receiver([post_save, post_delete], sender=SiteInfo)
def clear_page_cache(sender, instance, **kwargs):

    cache.delete(f"site_info:{getLang()}")
    cache.delete("site_status")
    cache.delete("site_maintenance_status")