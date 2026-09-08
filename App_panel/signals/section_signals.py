from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from App_panel.models.SectionModel import Section
from App_panel.models.PostModel import Post
from Admin_panel.helpers.client.Post import _invalidate_related_posts_cache_for_section


def bump_section_posts_version(section_slug):
    """
    بالا بردن ورژن کش لیست پست‌های یک سکشن خاص
    """
    version_key = f"section_posts_version:{section_slug}"
    ONE_MONTH = 2592000

    try:
        cache.incr(version_key)
    except ValueError:
        cache.set(version_key, 1, timeout=ONE_MONTH)


def clear_most_visited_section_cache(slug=None):
    """
    پاک کردن کش سکشن most visited.

    کلیدهای تابع:
    section_mostVisited:{slug}:days:{days}
    """
    if slug:
        cache.delete_pattern(f"*section_mostVisited:{slug}:days:*")
    else:
        cache.delete_pattern("*section_mostVisited:*:days:*")


@receiver([post_save, post_delete], sender=Section)
def section_changed_handler(sender, instance, **kwargs):
    _invalidate_related_posts_cache_for_section(instance.id)

    cache.delete(f"section_posts:{instance.slug}")
    cache.delete(f"section:{instance.slug}")
    bump_section_posts_version(instance.slug)

    clear_most_visited_section_cache(instance.slug)


@receiver(pre_save, sender=Post)
def store_old_section(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Post.objects.get(pk=instance.pk)
            instance._old_section = old_instance.section
        except Post.DoesNotExist:
            instance._old_section = None
    else:
        instance._old_section = None


@receiver(post_save, sender=Post)
def clear_section_posts_cache(sender, instance, **kwargs):
    if instance.section:
        cache.delete(f"section_posts:{instance.section.slug}")
        bump_section_posts_version(instance.section.slug)

    old_section = getattr(instance, "_old_section", None)

    if old_section and old_section != instance.section:
        cache.delete(f"section_posts:{old_section.slug}")
        bump_section_posts_version(old_section.slug)

    # چون پست جدید/ویرایش‌شده می‌تواند لیست پربازدیدها را تغییر دهد
    clear_most_visited_section_cache()


@receiver(post_delete, sender=Post)
def clear_section_posts_on_delete(sender, instance, **kwargs):
    if instance.section:
        cache.delete(f"section_posts:{instance.section.slug}")
        bump_section_posts_version(instance.section.slug)

    # حذف پست هم می‌تواند لیست پربازدیدها را تغییر دهد
    clear_most_visited_section_cache()
