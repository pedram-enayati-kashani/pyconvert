from django.http import Http404

class SuperAdminAccessRoutesMiddleware:
    ADMIN_PREFIXES = ("/app/",)
    EXCLUDED_PATHS = ("/app/login", "/app/login/")  # مسیرهایی که استثناء هستند

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith(self.ADMIN_PREFIXES) and path not in self.EXCLUDED_PATHS:

            user = request.user
            if not user.is_authenticated or not user.is_superuser:
                raise Http404

        return self.get_response(request)
