from django.apps import apps
from django.http import JsonResponse
from Admin_panel.helpers.model import generate_unique_slug

def get_slug(request):
    MODEL_MAP = {
        "section": ("App_panel", "Section"),
        "post": ("App_panel", "Post"),
        "cat": ("App_panel", "Category"),
        "tag": ("App_panel", "Tag"),
        "page": ("App_panel", "Page"),
    }

    text = request.GET.get("text")
    model_key = request.GET.get("model_key")
    instance_id = request.GET.get("instance_id")

    if model_key not in MODEL_MAP:
        return JsonResponse({"ok": False})

    app_label, model_name = MODEL_MAP[model_key]

    Model = apps.get_model(app_label, model_name)

    slug = generate_unique_slug(Model, text, instance_id)

    return JsonResponse({
        "ok": True,
        "slug": slug
    })
