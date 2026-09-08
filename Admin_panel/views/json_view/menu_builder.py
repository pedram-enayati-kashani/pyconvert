from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required
from Admin_panel.helpers.module.menu_builder import build_url_from_target

@staff_member_required
@require_GET
def resolve_menu_target(request):
    target = request.GET.get("address-list", "")
    url = build_url_from_target(target)

    return JsonResponse({
        "ok": bool(url),
        "url": url,
    })
