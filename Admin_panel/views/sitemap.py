# App_panel/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from App_panel.models.PostModel import Post
from App_panel.models.CategoriesModel import Category
from App_panel.models.TagModel import Tag
from App_panel.models.SectionModel import Section
from App_panel.models.PageModel import Page
from django.db.models import Q


class PostSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'
    limit = 1000

    def items(self):
        return Post.objects.filter(status='published').order_by("-id")

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'
    limit = 1000

    def items(self):
        return Category.objects.filter(status='published').order_by("-id")

    def location(self, obj):
        return reverse('Client:category', kwargs={'cat_slug': obj.slug})

    def lastmod(self, obj):
        return obj.updated_at

class TagSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'
    limit = 1000

    def items(self):
        return Tag.objects.filter(status='published').order_by("-id")

    def location(self, obj):
        return reverse('Client:tag', kwargs={'tag_slug': obj.slug})

    def lastmod(self, obj):
        return obj.updated_at

class SectionSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"
    limit = 1000

    def items(self):
        return (
            Section.objects
            .filter(status="active")
            .filter(
                Q(type="post") |
                Q(slug__in=["rent", "sell-buy"])
            )
            .order_by("-id")
        )

    def location(self, obj):
        special_routes = {
            "rent": "Client:rent",
            "sell-buy": "Client:sell-buy",
        }
        if obj.slug in special_routes:
            return reverse(special_routes[obj.slug])

        return reverse("Client:section", kwargs={"section_slug": obj.slug})

    def lastmod(self, obj):
        return obj.updated_at

class PagesSitemap(Sitemap):
    changefreq = 'weekly'
    limit = 1000

    def items(self):
        return Page.objects.filter(status='active').order_by("-id")

    def location(self, obj):
        if obj.slug == "home":
            return reverse("Client:home")
        elif obj.slug == "about":
            return reverse("Client:about")
        elif obj.slug == "contact":
            return reverse("Client:contact")
        else:
            return reverse("Client:page", kwargs={"page_slug": obj.slug})

    def priority(self, obj):
        if obj.slug == "home":
            return 1.0
        return 0.6

    def lastmod(self, obj):
        return obj.updated_at