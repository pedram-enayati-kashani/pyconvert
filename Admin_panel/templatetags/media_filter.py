import re
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from module.models.MediaModel import Media
from django.db.models import Q

register = template.Library()

SHORTCODE_PATTERN = re.compile(
    r'\[(?P<prefix>VID|SND|IMG)-(?P<key>[A-Fa-f0-9]+)\]'
)

@register.filter(name='render_shortcodes')
def render_shortcodes(value):
    if not value:
        return ""

    matches = list(SHORTCODE_PATTERN.finditer(value))
    if not matches:
        return mark_safe(value)

    keys = {m.group('key').upper() for m in matches}

    q = Q()
    for k in keys:
        q |= Q(media_key__iexact=k) | Q(media_key__icontains=k)

    media_items = Media.objects.filter(q).only(
        'id', 'media_key', 'media', 'title', 'status'
    )

    media_map = {}
    for item in media_items:
        stored = item.media_key.upper()
        token = stored.split('-')[-1]
        media_map[token] = item

    def replace_with_player(match):
        key = match.group('key').upper()
        media_item = media_map.get(key)
        if not media_item:
            return match.group(0)

        media_url = escape(media_item.media.url)
        title = escape(media_item.title or '')
        prefix = match.group('prefix')

        if prefix == 'VID':
            return (
                f'<div class="video-wrapper">'
                f'<video class="video-js vjs-default-skin js-video-player" '
                f'controls preload="metadata">'
                f'<source src="{media_url}" type="{media_item.video_mime_type}">'
                f'</video></div>'
            )

        if prefix == 'SND':
            return (
                f'<div class="audio-wrapper">'
                f'<audio class="video-js vjs-default-skin js-audio-player" '
                f'controls preload="metadata">'
                f'<source src="{media_url}" type="{media_item.sound_mime_type}">'
                f'</audio></div>'
            )
        if prefix == 'IMG':
            return f'<img src="{media_url}" alt="{title}" class="img-fluid" loading="lazy">'

        return match.group(0)

    return mark_safe(SHORTCODE_PATTERN.sub(replace_with_player, value))
