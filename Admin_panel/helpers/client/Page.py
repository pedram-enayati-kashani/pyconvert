from django.shortcuts import get_object_or_404
from django.core.cache import cache
from App_panel.models import Post
from App_panel.models.PageModel import Page


def getPage(slug):
    cache_key = f"page:{slug}"

    page = cache.get(cache_key)
    if page:
        return page

    page = get_object_or_404(
            Page.objects.filter(
                slug=slug,
                status="active",
            ).only("slug","title","body","title_seo","description_seo","image").order_by("id")
        )

    cache.set(cache_key, page, 600)

    return page

def getPostPage(slug, limit=None):
    cache_key = f"page_posts:{slug}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    page = get_object_or_404(
        Page.objects.only("id", "slug", "title", "body", "title_seo", "description_seo", "image"),
        slug=slug,
        status="active"
    )
    post_queryset = Post.objects.filter(status="published", pages=page).only(
        "id", "slug", "title", "body", "title_search", "summery_search", "image","watermark"
    ).order_by("-created_at")

    if limit:
        posts = list(post_queryset[:limit])
    else:
        posts = list(post_queryset)

    data = {
        "page": page,
        "posts": posts,
    }
    cache.set(cache_key, data, 600)
    return data

