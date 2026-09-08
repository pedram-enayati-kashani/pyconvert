from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from module.models.FormBuilder import FormField, FieldValue, Form, PostFormAssignment


def clear_cache_for_post_ids(post_ids):
    """Remove cached form data for the given post IDs."""
    for post_id in post_ids:
        cache_key = f"post_form_fields_{post_id}"
        cache.delete(cache_key)


@receiver([post_save, post_delete], sender=PostFormAssignment)
def clear_cache_on_assignment_change(sender, instance, **kwargs):
    """Clear cache when a form is assigned to or removed from a post."""
    clear_cache_for_post_ids([instance.post_id])


@receiver([post_save, post_delete], sender=Form)
def clear_cache_on_form_change(sender, instance, **kwargs):
    """Clear cache when the form itself changes, such as status updates."""
    post_ids = PostFormAssignment.objects.filter(form=instance).values_list("post_id", flat=True)
    clear_cache_for_post_ids(post_ids)


@receiver([post_save, post_delete], sender=FormField)
def clear_cache_on_field_change(sender, instance, **kwargs):
    """Clear cache when a form field is created, updated, or deleted."""
    if instance.form_id:
        post_ids = PostFormAssignment.objects.filter(form_id=instance.form_id).values_list("post_id", flat=True)
        clear_cache_for_post_ids(post_ids)


@receiver([post_save, post_delete], sender=FieldValue)
def clear_cache_on_value_change(sender, instance, **kwargs):
    """پاک‌سازی کش فیلدهای کاستوم همان نوشته."""
    if instance.post_id:
        clear_cache_for_post_ids([instance.post_id])
