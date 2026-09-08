from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.cache import cache

from App_panel.models.TagModel import Tag
from App_panel.models.PostModel import Post

from Admin_panel.helpers.client.Post import (
    _invalidate_related_posts_cache_for_post,
    invalidate_post_cache
)


def bump_tag_posts_version(tag_slug):
    """
    بالا بردن ورژن کش لیست پست‌های یک برچسب خاص
    """
    version_key = f"tag_posts_version:{tag_slug}"
    ONE_MONTH = 2592000
    try:
        cache.incr(version_key)
    except ValueError:
        cache.set(version_key, 1, timeout=ONE_MONTH)


@receiver([post_save, post_delete], sender=Tag)
def tag_changed_handler(sender, instance, **kwargs):
    """
    وقتی خود تگ تغییر می‌کند
    """
    try:
        bump_tag_posts_version(instance.slug)

        tagged_posts = Post.objects.filter(tags=instance).only("slug")

        for post in tagged_posts:
            invalidate_post_cache(post.slug)
            _invalidate_related_posts_cache_for_post(post.slug)

    except Exception:
        pass


@receiver([post_save, post_delete], sender=Post)
def post_changed_handler(sender, instance, **kwargs):
    """
    وقتی پستی حذف یا ویرایش می‌شود
    """
    try:
        for tag in instance.tags.all():
            bump_tag_posts_version(tag.slug)
    except Exception:
        pass


@receiver(m2m_changed, sender=Post.tags.through)
def post_tags_changed_update_cache(sender, instance, action, pk_set, **kwargs):
    """
    وقتی تگ‌های یک پست تغییر می‌کنند
    """
    if action in ["post_add", "post_remove", "post_clear"]:

        invalidate_post_cache(instance.slug)
        _invalidate_related_posts_cache_for_post(instance.slug)

        if pk_set:
            impacted_tags = Tag.objects.filter(pk__in=pk_set)

            for tag in impacted_tags:
                bump_tag_posts_version(tag.slug)

        for tag in instance.tags.all():
            bump_tag_posts_version(tag.slug)
