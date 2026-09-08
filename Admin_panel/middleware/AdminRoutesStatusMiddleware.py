from django.http import Http404
from django.core.cache import cache
from App_panel.models.SiteInfoModel import SiteInfo

class AdminRoutesStatusMiddleware:
    ADMIN_PREFIXES = ("/admin/")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith(self.ADMIN_PREFIXES):
            status = cache.get("site_status")

            if status is None:
                info = SiteInfo.objects.filter(id=1).only("status").first()
                status = info.status if info else "inactive"
                cache.set("site_status", status, 604800)

            if status != "active":
                raise Http404

        return self.get_response(request)
