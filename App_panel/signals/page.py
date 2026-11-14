from django.db.models.signals import post_save, post_delete, m2m_changed
from django.core.cache import cache
from django.dispatch import receiver
from App_panel.models.PageModel import Page
from Admin_panel.helpers.lang import getLang

@receiver([post_save, post_delete], sender=Page)
def clear_page_cache(sender, instance, **kwargs):
    cache.delete(f"page:{getLang()}:{instance.slug}")
    cache.delete(f"page_posts:{getLang()}:{instance.slug}")