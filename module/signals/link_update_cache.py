from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from ..models import Menu, Menu_Links
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Menu)
@receiver([post_save, post_delete], sender=Menu_Links)
def clear_menu_cache(sender, instance, **kwargs):
    cache.delete_pattern("menu_links_cache_*")