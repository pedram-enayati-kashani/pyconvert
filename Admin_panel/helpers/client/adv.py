from module.models.Advertising import AdvImage, AdvText
from App_panel.models.SectionModel import Section
from django.core.cache import cache


def get_adv_banners(section_slug):
    cache_key = f"adv_banners:{section_slug}"
    banners = cache.get(cache_key)

    if banners is None:
        banners = list(AdvImage.objects
           .filter(section__slug=section_slug, section__status="active", status="active")
           .only("id", "image", "url", "rel", "section","target_blank"))
        cache.set(cache_key, banners, 3600)
    return banners


def get_adv_text_with_section(section_slug):
    cache_key = f"adv_text:{section_slug}"
    data = cache.get(cache_key)

    if data is None:
        try:
            section_obj = Section.objects.get(slug=section_slug, status="active")
        except Section.DoesNotExist:
            return None
        texts = list(AdvText.objects
                     .filter(section=section_obj, status="active")
                     .only("id", "title", "url", "rel","target_blank"))

        data = {
            'section': section_obj,
            'texts': texts
        }
        cache.set(cache_key, data, 3600)

    return data