from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from App_panel.models.UsersModel import Users
from Admin_panel.helpers.client.Post import _invalidate_related_posts_cache_for_user

@receiver([post_save, post_delete], sender=Users)
def user_changed_handler(sender, instance, **kwargs):
    _invalidate_related_posts_cache_for_user(instance.pk)
