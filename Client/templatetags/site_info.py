from django import template
from Admin_panel.helpers.client.helper_client import get_site_info_value
register = template.Library()

@register.simple_tag
def site(key):
    return get_site_info_value(key)


@register.simple_tag
def title(title, default=""):
    site_title = get_site_info_value("title")
    if site_title and (title or default):
        if title:
            return site_title + " - " + title
        else:
            return site_title + " - " + default