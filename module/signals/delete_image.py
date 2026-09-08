from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from module.models.SocialMediaModel import SocialMedia
from module.models.Advertising import AdvImage
from module.models.WaterMarkModel import WaterMark
from module.models.MediaModel import Media


FILE_FIELDS_MAP = {
    SocialMedia: ["icon"],
    AdvImage: ["image"],
    WaterMark: ['image'],
    Media: ["media"],
}


def get_model_manager(sender):
    """
    If the model has all_objects, use it.
    So that there are no problems with soft delete.
    """
    return getattr(sender, "all_objects", sender.objects)


@receiver(pre_save)
def handle_delete_old_files(sender, instance, **kwargs):
    """
    Before saving:
    If the file has changed one of the defined fields,
    The previous file will be deleted.
    """
    if sender not in FILE_FIELDS_MAP:
        return

    if not instance.pk:
        return

    manager = get_model_manager(sender)

    try:
        old_instance = manager.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    file_fields = FILE_FIELDS_MAP.get(sender, [])

    for field_name in file_fields:
        old_file = getattr(old_instance, field_name, None)
        new_file = getattr(instance, field_name, None)

        if old_file and old_file != new_file:
            old_file.delete(save=False)


@receiver(post_delete)
def handle_delete_files_on_remove(sender, instance, **kwargs):
    """
    After the actual deletion of the record:
    All files defined for that model will be deleted.
    """
    if sender not in FILE_FIELDS_MAP:
        return

    file_fields = FILE_FIELDS_MAP.get(sender, [])

    for field_name in file_fields:
        file_obj = getattr(instance, field_name, None)
        if file_obj:
            file_obj.delete(save=False)
