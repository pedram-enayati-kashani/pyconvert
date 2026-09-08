from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from Admin_panel.helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin,SuperAdminMixin
from Admin_panel.mixin.module import ModuleActiveRequiredMixin
from Admin_panel.forms.FilterActive import FilterForm
from Admin_panel.forms.Module.Advertising import AdvTextForm
from module.models.Advertising import AdvText

class Index(AdminRequiredMixin,ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/Adv_text/index.html'
    module_name = "adv_text"
    paginate_by = 15
    model = AdvText
    context_object_name = 'AdvTexts'
    form_class = FilterForm

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class()
        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context

class Create(AdminRequiredMixin,ModuleActiveRequiredMixin,CreateView):
    template_name = 'admin_panel/module/Adv_text/create.html'
    model = AdvText
    module_name = "adv_text"
    form_class = AdvTextForm
    success_url = reverse_lazy('Admin_panel:adv-text')

class Update(AdminRequiredMixin,ModuleActiveRequiredMixin, UpdateView):
    template_name = 'admin_panel/module/Adv_text/edit.html'
    model = AdvText
    module_name = "adv_text"
    form_class = AdvTextForm
    success_url = reverse_lazy('Admin_panel:adv-text')

class Query(AdminRequiredMixin,ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/Adv_text/index.html'
    paginate_by = 15
    module_name = "adv_text"
    model = AdvText
    context_object_name = 'AdvTexts'
    form_class = FilterForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        queryset = super().get_queryset()
        if self.form.is_valid():
            status_filter = self.form.cleaned_data.get('status', 'all')
            if status_filter != 'all':
                queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form
        if 'paginator' in context and 'page_obj' in context:
            context['visible_page_numbers'] = get_visible_page_numbers(
                paginator=context['paginator'],
                page_obj=context['page_obj']
            )
        return context


class Active(AdminRequiredMixin,ModuleActiveRequiredMixin,View):
    model = AdvText
    module_name = "adv_text"
    success_url = reverse_lazy('Admin_panel:adv-text')
    def get(self, request, pk, *args, **kwargs):
        object = get_object_or_404(self.model, pk=pk)
        object.toggle_status()
        if object.status == 'active':
            messages.success(
                request,
                f"تبلیغ '{object.title}' فعال شد.",
            )
        else:
            messages.warning(
                request,
                f"تبلیغ '{object.title}' غیرفعال شد.",
            )

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(self.success_url)

class Delete(AdminRequiredMixin,ModuleActiveRequiredMixin, DeleteView):
    model = AdvText
    module_name = "adv_text"
    success_url = reverse_lazy('Admin_panel:adv-text')