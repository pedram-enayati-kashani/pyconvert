from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from App_panel.models.PageModel import Page
from App_panel.models.PostModel import Post
from App_panel.models.SectionModel import Section
from App_panel.models.TagModel import Tag
from App_panel.models.CategoriesModel import Category
from App_panel.models.UsersModel import Users
from App_panel.models.ContactUsModel import ContactMessage


FILE_FIELDS_MAP = {
    Post: ["image"],
    Section: ["image"],
    Category: ["image"],
    Tag: ["image"],
    Page: ["image"],
    Users: ["avatar"],
    ContactMessage: ["image"],
    # اگر بعداً مثلاً مدلی داشتی با چند فیلد:
    # SomeModel: ["image", "icon", "file"],
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
