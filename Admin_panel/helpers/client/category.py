from App_panel.models import Post, Category
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

def get_category_posts_all(slug, page, per_page=15):
    version_key = f"category_posts_version:{slug}"
    version = cache.get(version_key, 1)
    cache_key = f"category_posts:{slug}:v{version}:page:{page}"

    data = cache.get(cache_key)
    if data:
        return data

    category = get_object_or_404(
        Category.objects.filter(
            slug=slug,
            status="published"
        ).only("title","title_seo","image","description","description_seo","slug").order_by("id")
    )

    posts = (
        Post.objects
        .filter(categories=category, status="published")
        .only('title','image','summery','created_at','slug','watermark')
        .order_by("-updated_at")
    )

    paginator = Paginator(posts, per_page)
    page_obj = paginator.get_page(page)

    data = {
        "category": category,
        "paginator": paginator,
        "page_obj": page_obj,
        "posts": list(page_obj.object_list),
    }

    cache.set(cache_key, data, 600)

    return data
