from App_panel.mixin.Panel_auth import AppPanelRequiredMixin
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from ..helpers.pager import get_visible_page_numbers
from django.views.generic.list import ListView
from django.views.generic import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from ..forms.Group import GroupForm

class Index(AppPanelRequiredMixin, ListView):
    template_name = 'App_panel/Group_Permission/index.html'
    paginate_by = 15
    model = Group
    context_object_name = 'Groups'

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
    template_name = 'App_panel/Group_Permission/create.html'
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('App_panel:group')

class Update(AppPanelRequiredMixin, UpdateView):
    template_name = 'App_panel/Group_Permission/edit.html'
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('App_panel:group')

class Active(AppPanelRequiredMixin,View):
    model = Group
    success_url = reverse_lazy('Admin_panel:category')
    def get(self, request, pk, *args, **kwargs):
        group = get_object_or_404(self.model, pk=pk)
        group.extra.toggle_status()
        if group.extra.status == 'active':
            messages.success(
                request,
                f"دسته بندی '{group.name}' فعال شد.",
            )
        else:
            messages.warning(
                request,
                f"دسته بندی '{group.name}' غیرفعال شد.",
            )

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(self.success_url)

class Delete(AppPanelRequiredMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('App_panel:group')
    template_name = "App_panel/Group_Permission/delete.html"