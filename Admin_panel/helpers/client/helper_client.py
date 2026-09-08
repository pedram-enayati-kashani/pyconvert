from django.db.models import Q
from django.core.cache import cache
from App_panel.models.SiteInfoModel import SiteInfo
from App_panel.models.Modules import Modules
from module.models.MenuBuilder import Menu ,Menu_Links
from module.models.SocialMediaModel import SocialMedia

def get_site_info_value(key):
    """
    get site info
    key = title, logo, favicon, description_seo
    """
    site_info = cache.get("site_info")
    if not isinstance(site_info, dict):
        obj = SiteInfo.objects.filter(id=1).only(
            "title","title_seo", "logo", "description_seo","favicon","favicon_16","favicon_32","apple_touch_icon",
            "android_192","android_512","favicon_ico","robotsText","headMeta","footerScript"
        ).first()

        site_info = {}
        if obj:
            site_info = {
                "title": obj.title,
                "title_seo": obj.title_seo,
                "logo": obj.logo.url if obj.logo else None,
                "favicon": obj.favicon.url if obj.favicon else None,
                "favicon_16": obj.favicon_16.url if obj.favicon_16 else None,
                "favicon_32": obj.favicon_32.url if obj.favicon_32 else None,
                "apple_touch_icon": obj.apple_touch_icon.url if obj.apple_touch_icon else None,
                "android_192": obj.android_192.url if obj.android_192 else None,
                "android_512": obj.android_512.url if obj.android_512 else None,
                "favicon_ico": obj.favicon_ico.url if obj.favicon_ico else None,
                "description_seo": obj.description_seo,
                "robotsText": obj.robotsText,
                "headMeta": obj.headMeta,
                "footerScript": obj.footerScript,
            }

        cache.set("site_info", site_info, 14400)

    return site_info.get(key)

def Get_menu_builder_links(menu_name,link_name=None):
    """
    get menu builder links
    give header name and get links
    """
    module_active = Modules.objects.filter(name="Menu_Builder", status="active").exists()
    if not module_active:
        return {}

    # ۲. مدیریت کش
    cache_key = f"menu_links_cache_{menu_name}"
    result = cache.get(cache_key)

    if result is None:
        # ۳. پیدا کردن منو
        menu = Menu.objects.filter(name=menu_name, status='active').first()
        if not menu:
            return {}

        links = list(
            Menu_Links.objects
            .filter(
                status='active',
                Menu=menu,
                parent__isnull=True,
            )
            .exclude(Q(url__isnull=True) | Q(url=''))
            .prefetch_related('children')
            .order_by('order')
        )

        result = {
            'menu': menu,
            'links': links,
        }
        cache.set(cache_key, result, 14400)

    if link_name is not None:
        links = result.get("links", {})
        target_link = next((link for link in links if link.name == link_name), {})
        return target_link

    return result


def Get_social_media():
    """
    get social media
    """
    cache_key = "social_media:v1"
    data = cache.get(cache_key)

    if data is not None:
        return data

    queryset = (
        SocialMedia.objects
        .filter(status='active')
        .only("title", "name", "url", "rel", "icon","target_blank").order_by("id")
    )

    data = {}

    for item in queryset:
        data[item.name] = {
            "title": item.title,
            "url": item.url,
            "rel": item.rel,
            "target_blank": item.target_blank,
            "icon": item.icon.url if item.icon else None
        }

    cache.set(cache_key, data, 14400)
    return data