from django.core.cache import cache
from django.http import Http404
from App_panel.models.Modules import Modules


class ModuleRoutesStatusMiddleware:
    BASE_PREFIX = "/admin/module/"
    MODULE_PATH_MAP = {
        "form-builder": "form_builder",
        "social-media": "social_media",
        "menu-builder": "Menu_Builder",
        "adv-text": "adv_text",
        "adv-image": "adv_image",
        "redirect-rule":"redirect_rule",
        "real-estate": "Real_Estate",
        "media": "media",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith(self.BASE_PREFIX):
            remaining_path = path[len(self.BASE_PREFIX):]
            first_segment = remaining_path.split("/", 1)[0]
            module_name = self.MODULE_PATH_MAP.get(first_segment)
            if module_name:
                cache_key = f"module_status_{module_name}"
                status = cache.get(cache_key)

                if status is None:
                    status = (
                        Modules.objects
                        .filter(name=module_name)
                        .values_list("status", flat=True)
                        .first()
                    ) or "inactive"

                    cache.set(cache_key, status, 604800)

                if status != "active":
                    raise Http404

        return self.get_response(request)
