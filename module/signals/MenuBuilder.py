from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from Admin_panel.helpers.lang import getLang
from module.models.MenuBuilder import Menu, Menu_Links


# ==========================================
# سیگنال‌های مربوط به مدل Menu
# ==========================================

@receiver(post_save, sender=Menu)
def clear_menu_cache_on_save(sender, instance, created, **kwargs):
    """پاک کردن کش وقتی یک منو ساخته یا ویرایش می‌شود"""
    cache.delete(f"menu_links_cache_{getLang()}_{instance.name}")


@receiver(post_delete, sender=Menu)
def clear_menu_cache_on_delete(sender, instance, **kwargs):
    """پاک کردن کش وقتی یک منو حذف می‌شود"""
    cache.delete(f"menu_links_cache_{getLang()}_{instance.name}")


# ==========================================
# سیگنال‌های مربوط به مدل Menu_Links
# ==========================================

@receiver(post_save, sender=Menu_Links)
def clear_link_cache_on_save(sender, instance, created, **kwargs):
    """پاک کردن کش وقتی یک لینک ساخته یا ویرایش می‌شود"""
    if instance.Menu:
        cache.delete(f"menu_links_cache_{getLang()}_{instance.Menu.name}")


@receiver(post_delete, sender=Menu_Links)
def clear_link_cache_on_delete(sender, instance, **kwargs):
    """پاک کردن کش وقتی یک لینک حذف می‌شود"""
    if instance.Menu:
        cache.delete(f"menu_links_cache_{getLang()}_{instance.Menu.name}")