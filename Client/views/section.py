from Admin_panel.helpers.client.Section import get_section_posts_all
from Client.helpers.pager import get_visible_page_numbers
from Admin_panel.helpers.client.schema import post_page_schema
from django.views.generic import ListView

def sections(request):
    pass


class SectionView(ListView):
    template_name = "pages/section.html"
    context_object_name = "posts"
    def get_queryset(self):
        page = self.request.GET.get("page", 1)
        data = get_section_posts_all(
            self.kwargs.get("section_slug"),
            page,
            per_page=15
        )

        self.section = data["section"]
        self._cached_data = data
        return data["posts"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = self.section
        context["paginator"] = self._cached_data["paginator"]
        context["page_obj"] = self._cached_data["page_obj"]
        context["schema"] = post_page_schema(self.request, self.section, self.object_list)
        context['visible_page_numbers'] = get_visible_page_numbers(
            paginator=context['paginator'],
            page_obj=context['page_obj']
        )

        return context

