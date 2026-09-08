from django.conf import settings
from django.shortcuts import render
from django.core.cache import cache
from App_panel.models.SiteInfoModel import SiteInfo


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # مسیرهای مجاز
        if request.path.startswith(
            ("/app/login", settings.STATIC_URL, settings.MEDIA_URL)
        ):
            return self.get_response(request)

        if request.user.is_authenticated and request.user.is_superuser:
            return self.get_response(request)

        site_setting = cache.get("site_maintenance_status")

        if site_setting is None:
            site_setting = SiteInfo.objects.filter(status="active").first()
            cache.set("site_maintenance_status", site_setting, 300)

        if site_setting and site_setting.maintenance == "active":
            return render(
                request,
                "pages/maintenance.html",
                status=503
            )

        return self.get_response(request)
