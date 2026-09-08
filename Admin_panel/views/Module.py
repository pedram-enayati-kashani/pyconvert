from django.views.generic.list import ListView
from ..helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin
from App_panel.models.Modules import Modules


class Index(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/module/index.html'
    paginate_by = 15
    model = Modules
    context_object_name = 'modules'

    def get_queryset(self):
        query = super().get_queryset().order_by('created_at')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context