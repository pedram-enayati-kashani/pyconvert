from App_panel.models.PostModel import Post
from django.db.models import Q
from django.core.cache import cache
import urllib.parse

def get_result_query(query):
    if not query:
        return Post.objects.none()

    cache_key = f"search_results:{urllib.parse.quote(query)}"
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    results = Post.objects.filter(
        Q(title__icontains=query) |
        Q(body__icontains=query) |
        Q(summery__icontains=query) |
        Q(tags__title__icontains=query) |
        Q(categories__title__icontains=query) |
        Q(section__title__icontains=query)
    ).filter(status="published").distinct().order_by("-updated_at")
    results_list = list(results)
    cache.set(cache_key, results_list, 900)

    return results_list