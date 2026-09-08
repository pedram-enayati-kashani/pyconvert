from django.views.generic import UpdateView, CreateView, DeleteView, TemplateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from Admin_panel.mixin.auth import AdminRequiredMixin
from Admin_panel.mixin.module import ModuleActiveRequiredMixin
from Admin_panel.forms.Module.watermark import WaterMarkForm
from module.models.WaterMarkModel import WaterMark

class Index(AdminRequiredMixin, ModuleActiveRequiredMixin,TemplateView):
    template_name = 'admin_panel/module/watermark/index.html'
    module_name = "watermark"
    context_object_name = 'watermark'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = WaterMark.objects.filter(id=1).first()
        return context

class Create(AdminRequiredMixin,ModuleActiveRequiredMixin,CreateView):
    template_name = 'admin_panel/module/watermark/create.html'
    model = WaterMark
    module_name = "watermark"
    form_class = WaterMarkForm
    success_url = reverse_lazy('Admin_panel:watermark')

class Update(AdminRequiredMixin,ModuleActiveRequiredMixin, UpdateView):
    template_name = 'admin_panel/module/watermark/edit.html'
    model = WaterMark
    module_name = "watermark"
    form_class = WaterMarkForm
    context_object_name = 'watermark'
    success_url = reverse_lazy('Admin_panel:watermark')

    def get_object(self, queryset=None):
        return WaterMark.objects.filter(id=1).first()


class Active(AdminRequiredMixin,ModuleActiveRequiredMixin,View):
    model = WaterMark
    success_url = reverse_lazy('Admin_panel:watermark')
    module_name = "watermark"
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
    model = WaterMark
    module_name = "watermark"
    success_url = reverse_lazy('Admin_panel:watermark')