import re
from django.db.models import Prefetch
from django.core.cache import cache
from App_panel.models.PostModel import Post
from App_panel.models.CommentsModel import Comments
from django.utils.safestring import mark_safe
from module.models.MediaModel import Media


def get_approved_comments_qs():
    """Approved top-level comments with approved children."""
    return (
        Comments.objects
        .filter(status="approved", parent__isnull=True)
        .prefetch_related(
            Prefetch(
                "children",
                queryset=Comments.objects.filter(status="approved").order_by("created_at"),
                to_attr="subComments",
            )
        )
        .order_by("-created_at")
    )


def get_post_cache_version(slug):
    return cache.get(f"post_version:{slug}", 1)


def invalidate_post_cache(slug):
    key = f"post_version:{slug}"
    try:
        cache.incr(key)
    except ValueError:
        cache.set(key, 2)
    # print(f"Invalidated post cache version for slug: {slug}") # for debug


def get_post_details_with_relations(slug):
    """
    Fetch a published post by slug with related objects and approved comments.
    """
    version = get_post_cache_version(slug)
    cache_key = f"post:{slug}:v{version}"

    post = cache.get(cache_key)
    if post is not None:
        return post

    try:
        post = (
            Post.objects
            .select_related("section", "user")
            .prefetch_related(
                "categories",
                "tags",
                "gallery_items",
                Prefetch("comments", queryset=get_approved_comments_qs()),
            )
            .get(status="published", slug=slug)
        )
        post.body = process_media_shortcodes(post.body)
        cache.set(cache_key, post, timeout=600)
        return post
    except Post.DoesNotExist:
        return None


from django.core.cache import cache

def get_related_posts(slug):
    """
    Fetch related posts based on the first category of the current post.
    Results are cached.
    """
    cache_key = f"post_related:{slug}"
    related_posts = cache.get(cache_key)
    if related_posts is not None:
        return related_posts

    try:
        current_post = (
            Post.objects
            .prefetch_related("categories")
            .only("id", "slug", "status")
            .get(slug=slug, status="published")
        )

        first_category = current_post.categories.first()
        if not first_category:
            return Post.objects.none()

        related_posts = list(
            Post.objects
            .filter(categories=first_category, status="published")
            .exclude(pk=current_post.pk)
            .only("id", "title", "slug", "image", "summery", "created_at", "watermark")
            .order_by("-updated_at")[:10]
        )

        cache.set(cache_key, related_posts, 600)
        return related_posts

    except Post.DoesNotExist:
        return Post.objects.none()


def _invalidate_related_posts_cache_for_post(post_slug):
    """Clear post_related cache for a specific post."""
    cache.delete(f"post_related:{post_slug}")
    # print(f"Invalidated post_related cache for slug: {post_slug}") # برای دیباگ

def _invalidate_related_posts_cache_for_section(section_id):
    """
    Clear post_related cache for all posts in a section.
    """
    try:
        posts_in_section = Post.objects.filter(section_id=section_id, status="published").only("slug").order_by("id")
        for post in posts_in_section:
            _invalidate_related_posts_cache_for_post(post.slug)
    except Exception as e:
        # print(f"Error invalidating related posts cache for section {section_id}: {e}")
        pass

def _invalidate_related_posts_cache_for_user(user_id):
    """
    Clear post_related cache for all posts belonging to a user.
    """
    try:
        user_posts = Post.objects.filter(user_id=user_id, status="published").only("slug").order_by("id")
        for post in user_posts:
            _invalidate_related_posts_cache_for_post(post.slug)
    except Exception as e:
        # print(f"Error invalidating related posts cache for user {user_id}: {e}")
        pass

# Shortcode pattern: [VID-...] , [SND-...] , [IMG-...]
SHORTCODE_PATTERN = re.compile(
    r'\[(?P<prefix>VID|SND|IMG)-(?P<hex_key>[A-Fa-f0-9]+)\]'
)

def process_media_shortcodes(text_content):
    """
    Extract all media keys from the text, fetch them from the database,
    and replace each one with the appropriate tag (video/audio/image).
    """
    if not text_content:
        return text_content

    matches = list(SHORTCODE_PATTERN.finditer(text_content))
    if not matches:
        return text_content

    db_keys = {
        f"{m.group('prefix')}-{m.group('hex_key').upper()}"
        for m in matches
    }

    media_items = Media.objects.filter(media_key__in=db_keys)
    media_map = {item.media_key.upper(): item for item in media_items}

    def replace(match):
        prefix = match.group('prefix')
        full_key = f"{prefix}-{match.group('hex_key').upper()}"

        media = media_map.get(full_key)
        if not media or not media.media:
            return match.group(0)

        url = media.media.url
        title = media.title or ''

        if prefix == 'VID':
            mime_type = media.video_mime_type or 'video/mp4'
            return (
                f'<div class="video-wrapper">'
                f'<video class="video-js vjs-default-skin js-video-player" '
                f'controls preload="metadata" style="width:100%;max-width:100%;">'
                f'<source src="{url}" type="{mime_type}">'
                f'Your browser does not support video playback.'
                f'</video></div>'
            )

        if prefix == 'SND':
            mime_type = media.sound_mime_type or 'audio/mpeg'
            return (
                f'<div class="audio-wrapper">'
                f'<audio class="video-js vjs-default-skin js-audio-player" '
                f'controls preload="metadata" style="width:100%;">'
                f'<source src="{url}" type="{mime_type}">'
                f'Your browser does not support audio playback.'
                f'</audio></div>'
            )

        if prefix == 'IMG':
            return (
                f'<div class="image-wrapper">'
                f'<img src="{url}" alt="{title}" loading="lazy" style="max-width:100%;">'
                f'</div>'
            )

        return match.group(0)

    return SHORTCODE_PATTERN.sub(replace, text_content)