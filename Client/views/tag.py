from django.shortcuts import render, get_object_or_404
from Client.helpers.pager import get_visible_page_numbers
from Admin_panel.helpers.client.tag import get_tag_posts_all
from Admin_panel.helpers.client.schema import post_page_schema
from django.views.generic import ListView

def tags(request):
    pass

class TagView(ListView):
    template_name = "pages/tag.html"
    context_object_name = "posts"
    paginate_by = 15

    def get_queryset(self):
        page = self.request.GET.get("page", 1)

        data = get_tag_posts_all(
            self.kwargs.get("tag_slug"),
            page,
            self.paginate_by
        )

        self.tag = data["tag"]
        self._cached_data = data

        return data["posts"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tag"] = self.tag
        context["paginator"] = self._cached_data["paginator"]
        context["page_obj"] = self._cached_data["page_obj"]

        context["schema"] = post_page_schema(
            self.request,
            self.tag,
            self.object_list
        )

        context["visible_page_numbers"] = get_visible_page_numbers(
            paginator=context["paginator"],
            page_obj=context["page_obj"]
        )

        return context

