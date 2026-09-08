from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from module.models.SocialMediaModel import SocialMedia


CACHE_INVALIDATION = {
    SocialMedia: ["social_media:v1"],
}


def clear_cache_for_model(sender):
    cache_keys = CACHE_INVALIDATION.get(sender, [])
    for key in cache_keys:
        cache.delete(key)


@receiver(post_save)
def clear_cache_on_save(sender, **kwargs):
    clear_cache_for_model(sender)


@receiver(post_delete)
def clear_cache_on_delete(sender, **kwargs):
    clear_cache_for_model(sender)
