from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from App_panel.models.PostModel import Post
from App_panel.models.CommentsModel import Comments
from App_panel.models.SectionModel import Section
from App_panel.models.CategoriesModel import Category
from App_panel.models.TagModel import Tag
from django.core.cache import cache
from Admin_panel.helpers.client.Post import (
    invalidate_post_cache,
    _invalidate_related_posts_cache_for_post,
    _invalidate_related_posts_cache_for_section,
    _invalidate_related_posts_cache_for_user
)
from App_panel.signals.section_signals import clear_most_visited_section_cache

def touch_section(section_id):
    try:
        Section.objects.filter(id=section_id).update(posts_updated_at=timezone.now())
    except Section.DoesNotExist:
        pass


@receiver([post_save, post_delete], sender=Post)
def post_save_or_delete_handler(sender, instance, **kwargs):
    invalidate_post_cache(instance.slug)
    _invalidate_related_posts_cache_for_post(instance.slug)
    cache.delete(f"post_form_fields_{instance.id}")
    clear_most_visited_section_cache(instance.section.slug)
    if instance.pages_id and instance.pages and instance.pages.slug:
        cache.delete(f"page_posts:{instance.pages.slug}")
    if instance.section_id:
        touch_section(instance.section_id)
    if kwargs.get('created'):
        pass

@receiver([post_save, post_delete], sender=Comments)
def clear_post_cache_on_comment_change(sender, instance, **kwargs):
    if instance.post and instance.post.slug:
        invalidate_post_cache(instance.post.slug)
        _invalidate_related_posts_cache_for_post(instance.post.slug)


@receiver(m2m_changed, sender=Post.tags.through)
def clear_post_cache_on_tags_change(sender, instance, **kwargs):
    invalidate_post_cache(instance.slug)
    _invalidate_related_posts_cache_for_post(instance.slug)

@receiver(m2m_changed, sender=Post.categories.through)
def clear_post_cache_on_categories_change(sender, instance, **kwargs):
    invalidate_post_cache(instance.slug)
    _invalidate_related_posts_cache_for_post(instance.slug)
