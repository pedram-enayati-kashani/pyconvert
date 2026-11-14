from django.utils.translation import get_language
from django.conf import settings

def getLang():
    lang = get_language()
    available_langs = [code for code, name in settings.LANGUAGES]
    if lang not in available_langs:
        lang = 'fa'
    return lang