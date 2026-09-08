import os
from django.core.files.storage import FileSystemStorage
from django.apps import apps
from Client.middleware.head_request import get_current_model_info


class CKEditorStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        info = get_current_model_info()

        if info:
            short_name = str(info['model']).lower()
            object_id = str(info['id'])
            get_correct_model_name = {
                "post": "Post",
                "cat": "Category",
                "tag": "Tag",
                "sec": "Section",
                "user": "Users",
                "page": "Page",
                "info": "SiteInfo",
                "comment": "Comments",
                "contact": "ContactMessage",
            }

            real_model_name = get_correct_model_name.get(short_name)

            if real_model_name:
                target_model = None
                for app_config in apps.get_app_configs():
                    try:
                        target_model = app_config.get_model(real_model_name)
                        break
                    except LookupError:
                        continue

                if object_id == 'new' and target_model:
                    try:
                        last_obj = target_model.objects.only('id').order_by('-id').first()
                        if last_obj:
                            object_id = str(last_obj.id + 1)
                        else:
                            object_id = "1"
                    except Exception:
                        object_id = 'new'
            name = os.path.join('ck', short_name, object_id, name)

        return super().get_available_name(name, max_length)
