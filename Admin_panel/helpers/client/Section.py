from App_panel.models import Post, Section
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from Admin_panel.helpers.client.most_visited import get_popular_by_days

def GetSecPosts(slug):
    """get posts of section"""

    cache_key = f"section_posts:{slug}"
    data = cache.get(cache_key)
    if data:
        return data

    section = Section.objects.filter(slug=slug,status="active",type="post").first()
    if not section:
        return {}
    posts = (
        Post.objects
        .filter(status="published", section=section)
        .select_related("user")
        .prefetch_related("tags", "categories")
        .order_by("-updated_at")[:section.display_number]
    )

    data = {
        "posts": list(posts),
        "section": section,
    }

    cache.set(cache_key, data, 600)
    return data

def get_section_posts_all(section_slug, page, per_page=15):
    version_key = f"section_posts_version:{section_slug}"
    version = cache.get(version_key, 1)
    cache_key = f"section_posts:{section_slug}:v{version}:page:{page}"

    data = cache.get(cache_key)
    if data:
        return data

    section = get_object_or_404(
            Section.objects.filter(
            slug=section_slug,
            status="active",
            type = "post")
            .only('title','title_seo','image','description','description_seo','slug').order_by("id")
    )

    posts = (
        Post.objects
        .filter(section=section, status="published")
        .only('title','image','summery','created_at','slug','watermark')
        .order_by("-updated_at")
    )

    paginator = Paginator(posts, per_page)
    page_obj = paginator.get_page(page)

    data = {
        "section": section,
        "paginator": paginator,
        "page_obj": page_obj,
        "posts": list(page_obj.object_list),
    }

    cache.set(cache_key, data, 600)

    return data



def GetSection(slug):
    cache_key = f"section:{slug}"
    data = cache.get(cache_key)
    if data:
        return data
    section = Section.objects.filter(slug=slug, status="active", type="no_post").first()

    data = {
        "section": section,
    }

    cache.set(cache_key, data, 600)
    return data

def GetMostVisitedSection(slug, days=30):
    cache_key = f"section_mostVisited:{slug}:days:{days}"
    data = cache.get(cache_key)
    if data is not None:
        return data

    section = Section.objects.filter(slug=slug, status="active").first()
    if not section:
        data = {
            "section": None,
            "posts": [],
        }
        cache.set(cache_key, data, 600)
        return data

    posts = get_popular_by_days(days=days, limit=section.display_number)
    data = {
        "section": section,
        "posts": posts,
    }
    cache.set(cache_key, data, 600)

    return data