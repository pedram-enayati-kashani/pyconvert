from django import template
from django.core.cache import cache
from Admin_panel.helpers.client.watermark import get_watermark
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

register = template.Library()

@register.simple_tag
def wm_version():
    watermark = get_watermark()

    if watermark:
        return watermark.version

    return 1

@register.simple_tag
def render_post_image(post,width,height):
    image_path = post.image if post.image else "defaults/demo.png"
    is_active = getattr(post, 'watermark', 'inactive') == 'active'
    options = {
        "format": "WEBP",
        "quality": 95,
        "crop": "center",
    }
    if is_active:
        options["watermark"] = True
    im = get_thumbnail(image_path, f"{width}x{height}", **options)
    html = f'''<img src="{im.url}" alt="{getattr(post, 'title', 'تصویر')}" 
               title="{getattr(post, 'title', 'تصویر')}" decoding="async" 
               width="{width}" height="{height}">'''

    return mark_safe(html)

@register.simple_tag
def render_post_image_gallery(post,item,width,height):
    image_path = item.image if item.image else "defaults/demo.png"
    is_active = getattr(post, 'watermark', 'inactive') == 'active'
    options = {
        "format": "WEBP",
        "quality": 95,
        "crop": "center",
    }
    if is_active:
        options["watermark"] = True
    im = get_thumbnail(image_path, f"{width}x{height}", **options)
    html = f'''<img src="{im.url}" alt="{getattr(item, 'alt_text', 'تصویر')}" 
               title="{getattr(item, 'alt_text', 'تصویر')}" decoding="async" 
               width="{width}" height="{height}">'''

    return mark_safe(html)
