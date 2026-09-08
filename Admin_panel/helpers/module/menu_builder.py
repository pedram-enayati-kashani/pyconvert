from django.urls import reverse, NoReverseMatch
from App_panel.models.PageModel import Page
from App_panel.models.CategoriesModel import Category
from App_panel.models.SectionModel import Section

def build_url_from_target(target):
    if not target:
        return None

    target = str(target).strip()

    if target == "robots":
        return "/robots.txt"
    if target == "sitemap":
        return "/sitemap.xml"

    if "_" not in target:
        return None

    target_type, target_id_str = target.split("_", 1)

    try:
        target_id = int(target_id_str)
    except (TypeError, ValueError):
        return None

    try:
        if target_type == "page":
            obj = Page.objects.filter(id=target_id, status="active").only("slug").first()
            if not obj or not obj.slug:
                return None

            special_pages = {
                "home": "Client:home",
                "about": "Client:about",
                "contact": "Client:contact",
            }
            if obj.slug in special_pages:
                return reverse(special_pages[obj.slug])

            return reverse("Client:page", kwargs={"page_slug": obj.slug})

        if target_type == "cate":
            obj = Category.objects.filter(id=target_id, status="published").only("slug").first()
            if not obj or not obj.slug:
                return None
            return reverse("Client:category", kwargs={"cat_slug": obj.slug})

        if target_type == "sec":
            obj = Section.objects.filter(id=target_id, status="active").only("slug").first()
            if not obj or not obj.slug:
                return None
            return reverse("Client:section", kwargs={"section_slug": obj.slug})

    except NoReverseMatch:
        return None

    return None
