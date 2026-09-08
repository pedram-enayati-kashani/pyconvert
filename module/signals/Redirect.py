from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from module.models import RedirectRule


def get_redirect_cache_key(path):
    return f"redirect_rule:{path}"


@receiver(post_save, sender=RedirectRule)
def clear_redirect_cache_on_save(sender, instance, **kwargs):
    cache.delete(get_redirect_cache_key(instance.old_url))
    original_old_url = getattr(instance, "_original_old_url", None)
    if original_old_url and original_old_url != instance.old_url:
        cache.delete(get_redirect_cache_key(original_old_url))
    instance._original_old_url = instance.old_url


@receiver(post_delete, sender=RedirectRule)
def clear_redirect_cache_on_delete(sender, instance, **kwargs):
    cache.delete(get_redirect_cache_key(instance.old_url))
