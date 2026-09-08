from App_panel.mixin.Panel_auth import AppPanelRequiredMixin
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from ..helpers.pager import get_visible_page_numbers
from django.views.generic.list import ListView
from django.views.generic import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from ..models.Modules import Modules
from ..forms.Module import ModuleForm
from django.core.cache import cache

class Index(AppPanelRequiredMixin, ListView):
    template_name = 'App_panel/modules/index.html'
    paginate_by = 15
    model = Modules
    context_object_name = 'modules'

    def get_queryset(self):
        query = super().get_queryset().order_by('-id')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context

class Create(AppPanelRequiredMixin,CreateView):
    template_name = 'App_panel/modules/create.html'
    model = Modules
    form_class = ModuleForm
    success_url = reverse_lazy('App_panel:module')

class Update(AppPanelRequiredMixin, UpdateView):
    template_name = 'App_panel/modules/edit.html'
    model = Modules
    form_class = ModuleForm
    context_object_name = 'module'
    success_url = reverse_lazy('App_panel:module')

class Active(AppPanelRequiredMixin,View):
    model = Modules
    success_url = reverse_lazy('App_panel:module')
    def get(self, request, pk, *args, **kwargs):
        module = get_object_or_404(self.model, pk=pk)
        module.toggle_status()
        if module.status == 'active':
            messages.success(
                request,
                f"ماژول '{module.title}' فعال شد.",
            )
        else:
            messages.warning(
                request,
                f"ماژول '{module.title}' غیرفعال شد.",
            )
        cache.delete("form_builder_status")
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(self.success_url)

class Delete(AppPanelRequiredMixin, DeleteView):
    model = Modules
    success_url = reverse_lazy('App_panel:module')