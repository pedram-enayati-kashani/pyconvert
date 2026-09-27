from django.conf import settings
from Admin_panel.helpers.client.helper_client import get_site_info_value
import json

def clean_schema(obj):
    if isinstance(obj, dict):
        return {k: clean_schema(v) for k, v in obj.items() if v not in [None, "", [], {}]}
    elif isinstance(obj, list):
        return [clean_schema(item) for item in obj if item not in [None, "", [], {}]]
    return obj


def base_schema(data):
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{data['base_url']}/#organization",
                "name": data["organization_name"],
                "url": data["base_url"],
                "logo": {
                    "@type": "ImageObject",
                    "url": data["logo"]
                } if data.get("logo") else None,
            },
            {
                "@type": "WebSite",
                "@id": f"{data['base_url']}/#website",
                "url": data["base_url"],
                "name": data["site_title"],
                "publisher": {
                    "@id": f"{data['base_url']}/#organization"
                }
            }
        ]
    }


def news_article_schema(data):
    return {
        "@type": "NewsArticle",
        "@id": f"{data['post_url']}#article",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": data["post_url"]
        },
        "headline": data["post_title"],
        "description": data["post_description"],
        "image": [data["post_image"]] if data.get("post_image") else [],
        "datePublished": data["post_created_at"],
        "dateModified": data["post_updated_at"],
        "author": {
            "@type": "Person",
            "name": data["post_author"]
        },
        "publisher": {
            "@id": f"{data['base_url']}/#organization"
        }
    }


def product_schema(data):
    return {
        "@type": "Product",
        "@id": f"{data['post_url']}#product",
        "name": data["post_title"],
        "url": data["post_url"],
        "image": [data["post_image"]] if data.get("post_image") else [],
        "description": data["post_description"],
        "offers": {
            "@type": "Offer",
            "price": data["post_price"],
            "priceCurrency": data["post_currency"],
            "availability": "https://schema.org/InStock",
            "url": data["post_url"],
        }
    }


def classified_schema(data):
    return {
        "@type": "Product",
        "@id": f"{data['post_url']}#classified",
        "name": data["post_title"],
        "url": data["post_url"],
        "image": [data["post_image"]] if data.get("post_image") else [],
        "description": data["post_description"],
        "offers": {
            "@type": "Offer",
            "price": data["post_price"],
            "priceCurrency": data["post_currency"],
            "url": data["post_url"],
        }
    }


def collection_page_schema(data, posts):
    item_list = []

    for index, post in enumerate(posts[:10], start=1):
        item_list.append({
            "@type": "ListItem",
            "position": index,
            "url": post["url"],
            "name": post["title"],
        })

    return {
        "@type": "CollectionPage",
        "@id": f"{data['page_url']}#collection",
        "url": data["page_url"],
        "name": data["page_title"],
        "description": data["page_description"],
        "isPartOf": {
            "@id": f"{data['base_url']}/#website"
        },
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": item_list
        }
    }

def web_page_schema(data):
    return {
        "@type": "WebPage",
        "@id": f"{data['page_url']}#webpage",
        "url": data["page_url"],
        "name": data["page_title"],
        "description": data["page_description"],
        "isPartOf": {
            "@id": f"{data['base_url']}/#website"
        },
        "publisher": {
            "@id": f"{data['base_url']}/#organization"
        }
    }

def get_post_schema(data, related_posts=None):
    """
    Generate structured data for a single content/detail page.

    Used for:
    - News article pages
    - Blog post pages
    - Product detail pages
    - Classified ad pages

    Args:
        data (dict): A dictionary containing the page, item, and site metadata
            required to build the schema.
        related_posts (list[dict], optional): A list of related items to include
            as an ItemList in the schema.

    Returns:
        dict: A JSON-LD schema graph for a single item/detail page.
    """
    full_schema = base_schema(data)
    mode = getattr(settings, "SITE_MODE", "news")

    if mode == "news":
        full_schema["@graph"].append(news_article_schema(data))
    elif mode == "shop":
        full_schema["@graph"].append(product_schema(data))
    elif mode == "classified":
        full_schema["@graph"].append(classified_schema(data))

    if related_posts:
        full_schema["@graph"].append({
            "@type": "ItemList",
            "name": "مطالب مرتبط",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": index,
                    "url": post["url"],
                    "name": post["title"],
                }
                for index, post in enumerate(related_posts[:10], start=1)
            ]
        })

    return clean_schema(full_schema)

def get_collection_schema(data, posts):
    """
    Generate schema for pages that display a list of posts/items.

    Used for:
    - Home page
    - Category pages
    - Tag pages
    - Section pages
    - Archive pages
    - Search result pages

    Args:
        data (dict): General page/site information.
        posts (list): List of post dictionaries.

    Returns:
        dict: JSON-LD schema graph for a collection page.
    """
    full_schema = base_schema(data)
    full_schema["@graph"].append(collection_page_schema(data, posts))
    return clean_schema(full_schema)

def get_page_schema(data):
    """
        Generate structured data for a static website page.

    Used for:
    - About Us page
    - Contact Us page
    - Terms and Conditions page
    - Other static CMS pages

    Args:
        data (dict): A dictionary containing the page and site metadata
            required to build the schema.

    Returns:
        dict: A JSON-LD schema graph for a static web page.
    """
    full_schema = base_schema(data)
    full_schema["@graph"].append(web_page_schema(data))
    return clean_schema(full_schema)

def homePageSchema(request,data):
    schema_data = {
        "base_url": f"{request.scheme}://{request.get_host()}",
        "organization_name": get_site_info_value("title"),
        "logo": f"{request.scheme}://{request.get_host()}/{get_site_info_value('logo').lstrip('/')}",
        "site_title": get_site_info_value("title_seo") or get_site_info_value("title")[:60],
        "page_url": f"{request.scheme}://{request.get_host()}/",
        "page_title": get_site_info_value("title_seo") or get_site_info_value("title")[:60],
        "page_description": get_site_info_value("description_seo"),
    }

    posts_data = [
        {
            "url": f"{request.scheme}://{request.get_host()}{item.get_absolute_url()}",
            "title": getattr(item, "title_search", None) or item.title[:60],
        }
        for item in data["posts"]
    ]

    schema = get_collection_schema(schema_data, posts_data)
    if schema:
        return json.dumps(schema, ensure_ascii=False)
    else:
        return ""

def singlePostSchema(request,post,related_posts):
    schema_data = {
        "base_url": f"{request.scheme}://{request.get_host()}",
        "organization_name": get_site_info_value("title"),
        "logo": f"{request.scheme}://{request.get_host()}/{get_site_info_value('logo').lstrip('/')}",
        "site_title": get_site_info_value("title_seo"),

        "post_url": f"{request.scheme}://{request.get_host()}{post.get_absolute_url()}",
        "post_title": post.title_search or post.title,
        "post_description": post.summery_search or (post.summery[:160] if post.summery else ""),
        "post_image": f"{request.scheme}://{request.get_host()}{post.image.url}" if post.image else "",
        "post_created_at": post.created_at.isoformat(),
        "post_updated_at": post.updated_at.isoformat(),
        "post_author": str(post.user),
        "post_price": getattr(post, "price", 0),
        "post_currency": "IRT",
    }

    related_posts_data = [
        {
            "url": f"{request.scheme}://{request.get_host()}{item.get_absolute_url()}",
            "title": item.title_search or item.title,
        }
        for item in related_posts[:10]
    ]

    schema = get_post_schema(schema_data, related_posts=related_posts_data)
    return json.dumps(schema, ensure_ascii=False) if schema else ""

def post_page_schema(request,page,posts):
    schema_data = {
        "base_url": f"{request.scheme}://{request.get_host()}",
        "organization_name": get_site_info_value("title"),
        "logo": f"{request.scheme}://{request.get_host()}/{get_site_info_value('logo').lstrip('/')}",
        "site_title": get_site_info_value("title_seo") or get_site_info_value("title")[:60],

        "page_url": f"{request.scheme}://{request.get_host()}{page.get_absolute_url()}",
        "page_title": page.title_seo or page.title[:60],
        "page_description": page.description_seo or page.description[:160],
    }

    posts_data = [
        {
            "url": f"{request.scheme}://{request.get_host()}{item.get_absolute_url()}",
            "title": getattr(item, "title_search", None) or item.title[:60],
        }
        for item in posts
    ]

    schema = get_collection_schema(schema_data, posts_data)
    return json.dumps(schema, ensure_ascii=False) if schema else ""

def page_schema(request,page):
    if not page:
        return ""
    if page.slug in ["about","contact"]:
        page_url = f"{request.scheme}://{request.get_host()}/{page.slug}"
    else:
        page_url = f"{request.scheme}://{request.get_host()}{page.get_absolute_url()}"
    data = {
        "base_url": f"{request.scheme}://{request.get_host()}",
        "organization_name": get_site_info_value("title"),
        "logo": f"{request.scheme}://{request.get_host()}/{get_site_info_value('logo').lstrip('/')}",
        "site_title": get_site_info_value("title_seo") or (get_site_info_value("title") or "")[:60],

        "page_url": page_url,
        "page_title": page.title_seo or page.title[:60],
        "page_description": page.description_seo,
    }

    schema = get_page_schema(data)
    return json.dumps(schema, ensure_ascii=False) if schema else ""