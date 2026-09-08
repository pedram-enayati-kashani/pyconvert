from django.utils import translation
from django.conf import settings


class SmartUrlLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language_from_path = translation.get_language_from_path(request.path_info)

        if language_from_path:
            translation.activate(language_from_path)
            request.LANGUAGE_CODE = language_from_path
        else:
            user_cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
            if user_cookie_lang:
                translation.activate(user_cookie_lang)
                request.LANGUAGE_CODE = user_cookie_lang
            else:
                translation.activate(settings.LANGUAGE_CODE)
                request.LANGUAGE_CODE = settings.LANGUAGE_CODE

        response = self.get_response(request)
        return response
