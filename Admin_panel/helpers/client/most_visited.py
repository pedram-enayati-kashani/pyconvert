import hashlib
from django_redis import get_redis_connection
from App_panel.models.PostModel import Post
from django.utils import timezone
from django.db.models import Case, When
from django.core.cache import cache
from datetime import timedelta
from django.conf import settings

def get_redis():
    return get_redis_connection("default")

def get_client_ip(request):
    cf_ip = request.META.get("HTTP_CF_CONNECTING_IP")
    if cf_ip:
        return cf_ip

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def hash_ip(ip):
    value = f"{ip}:{settings.SECRET_KEY}"
    return hashlib.sha256(value.encode()).hexdigest()


def increase_post_views(request, post_id):
    redis_conn = get_redis()

    ip = get_client_ip(request)
    ip_hash = hash_ip(ip) if ip else "unknown"

    if request.user.is_authenticated:
        viewer_id = f"user:{request.user.id}:{ip_hash}"
    else:
        session_key = request.session.session_key

        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        viewer_id = f"anon:{session_key}:{ip_hash}"

    prefix = settings.REDIS_KEY_PREFIX
    viewer_key = f"{prefix}:most_visited_post:viewed:{post_id}:{viewer_id}"

    was_set = redis_conn.set(viewer_key, 1, ex=60 * 30, nx=True)

    if not was_set:
        return False

    redis_conn.zincrby(f"{prefix}:most_visited_post:views:total", 1, post_id)

    today = timezone.now().strftime("%Y-%m-%d")
    daily_key = f"{prefix}:most_visited_post:views:daily:{today}"

    redis_conn.zincrby(daily_key, 1, post_id)
    redis_conn.expire(daily_key, 60 * 60 * 24 * 45)

    return True


def get_popular_by_days(days=1, limit=5):
    redis_conn = get_redis()

    today = timezone.now().date()

    keys = []

    for i in range(days):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        keys.append(f"{settings.REDIS_KEY_PREFIX}:most_visited_post:views:daily:{date}")

    if not keys:
        return []

    temp_key = f"{settings.REDIS_KEY_PREFIX}:most_visited_post:views:temp:{days}:limit:{limit}"

    redis_conn.zunionstore(temp_key, keys)
    redis_conn.expire(temp_key, 10)

    post_items = redis_conn.zrevrange(
        temp_key,
        0,
        limit - 1,
        withscores=True
    )

    if not post_items:
        return []

    post_ids = [int(post_id) for post_id, score in post_items]

    views_map = {
        int(post_id): int(score)
        for post_id, score in post_items
    }

    preserved = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(post_ids)]
    )

    posts = list(
        Post.objects.filter(
            id__in=post_ids,
            status="published"
        ).order_by(preserved)
    )

    for post in posts:
        post.period_views = views_map.get(post.id, 0)

    return posts

def get_posts_total_views(post_ids):
    redis_conn = get_redis()
    key = f"{settings.REDIS_KEY_PREFIX}:most_visited_post:views:total"

    if not post_ids:
        return {}

    values = redis_conn.zmscore(key, post_ids)

    return {
        int(post_id): int(score or 0)
        for post_id, score in zip(post_ids, values)
    }


