from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.cache import cache

from App_panel.models.CategoriesModel import Category
from App_panel.models.PostModel import Post
from Admin_panel.helpers.client.Post import _invalidate_related_posts_cache_for_post, invalidate_post_cache

def bump_category_posts_version(slug):
    """
    بالا بردن ورژن کش لیست پست‌های یک دسته خاص
    """
    version_key = f"category_posts_version:{slug}"
    ONE_MONTH = 2592000
    try:
        cache.incr(version_key)
    except ValueError:
        cache.set(version_key, 1, timeout=ONE_MONTH)

@receiver([post_save, post_delete], sender=Category)
def category_changed_handler(sender, instance, **kwargs):
    """
    وقتی خود دسته تغییر می‌کند (مثلاً نام یا اسلاگش)
    """
    try:
        bump_category_posts_version(instance.slug)
        categorized_posts = Post.objects.filter(categories=instance).only("slug")
        for post in categorized_posts:
            invalidate_post_cache(post.slug)
            _invalidate_related_posts_cache_for_post(post.slug)

    except Exception:
        pass

@receiver([post_save, post_delete], sender=Post)
def post_changed_handler(sender, instance, **kwargs):
    """
    وقتی پستی حذف یا ویرایش می‌شود، باید لیست تمام دسته‌هایی که عضو است آپدیت شود
    """
    try:
        for category in instance.categories.all():
            bump_category_posts_version(category.slug)
    except Exception:
        pass

@receiver(m2m_changed, sender=Post.categories.through)
def post_categories_changed_update_cache(sender, instance, action, pk_set, **kwargs):
    """
    وقتی دسته‌های یک پست را کم یا زیاد می‌کنیم
    """
    if action in ["post_add", "post_remove", "post_clear"]:
        invalidate_post_cache(instance.slug)
        _invalidate_related_posts_cache_for_post(instance.slug)
        if pk_set:
            impacted_categories = Category.objects.filter(pk__in=pk_set)
            for cat in impacted_categories:
                bump_category_posts_version(cat.slug)
        for cat in instance.categories.all():
            bump_category_posts_version(cat.slug)
