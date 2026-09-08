from Client.helpers.pager import get_visible_page_numbers
from Admin_panel.helpers.client.category import get_category_posts_all
from django.views.generic import ListView
from Admin_panel.helpers.client.schema import post_page_schema

def categories(request):
    pass

class CategoryView(ListView):
    template_name = "pages/category.html"
    context_object_name = "posts"
    paginate_by = 15

    def get_queryset(self):
        page = self.request.GET.get("page", 1)

        data = get_category_posts_all(
            self.kwargs.get("cat_slug"),
            page,
            self.paginate_by
        )

        self.category = data["category"]
        self._cached_data = data

        return data["posts"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paginator"] = self._cached_data["paginator"]
        context["page_obj"] = self._cached_data["page_obj"]
        context["category"] = self.category
        context["schema"] = post_page_schema(
            self.request,
            self.category,
            self.object_list
        )
        if 'paginator' in context and 'page_obj' in context:
            context['visible_page_numbers'] = get_visible_page_numbers(
                paginator=context['paginator'],
                page_obj=context['page_obj']
            )

        return context