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
from Admin_panel.forms.Module.Advertising import AdvImageForm
from module.models.Advertising import AdvImage

class Index(AdminRequiredMixin, ModuleActiveRequiredMixin,ListView):
    template_name = 'admin_panel/module/Adv_image/index.html'
    module_name = "adv_image"
    paginate_by = 15
    model = AdvImage
    context_object_name = 'AdvImage'
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
    template_name = 'admin_panel/module/Adv_image/create.html'
    model = AdvImage
    module_name = "adv_image"
    form_class = AdvImageForm
    success_url = reverse_lazy('Admin_panel:adv-image')

class Update(AdminRequiredMixin,ModuleActiveRequiredMixin, UpdateView):
    template_name = 'admin_panel/module/Adv_image/edit.html'
    model = AdvImage
    module_name = "adv_image"
    form_class = AdvImageForm
    context_object_name = 'AdvImage'
    success_url = reverse_lazy('Admin_panel:adv-image')

class Query(AdminRequiredMixin, ModuleActiveRequiredMixin,ListView):
    template_name = 'admin_panel/module/Adv_image/index.html'
    paginate_by = 15
    model = AdvImage
    module_name = "adv_image"
    context_object_name = 'AdvImage'
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
    model = AdvImage
    success_url = reverse_lazy('Admin_panel:adv-image')
    module_name = "adv_image"
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
    model = AdvImage
    module_name = "adv_image"
    success_url = reverse_lazy('Admin_panel:adv-image')