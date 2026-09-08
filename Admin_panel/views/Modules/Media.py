from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from Admin_panel.helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin
from Admin_panel.mixin.module import ModuleActiveRequiredMixin
from Admin_panel.forms.FilterActive import FilterForm
from Admin_panel.forms.Module.media import MediaForm
from module.models.MediaModel import Media

class Index(AdminRequiredMixin,ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/media/index.html'
    paginate_by = 15
    model = Media
    module_name = "media"
    context_object_name = 'media'
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

class Show(AdminRequiredMixin,ModuleActiveRequiredMixin,DetailView):
    model = Media
    template_name = 'admin_panel/module/media/show.html'
    context_object_name = 'media_object'
    module_name = "media"
    form_class = MediaForm

class Create(AdminRequiredMixin,ModuleActiveRequiredMixin,CreateView):
    template_name = 'admin_panel/module/media/create.html'
    model = Media
    module_name = "media"
    form_class = MediaForm
    success_url = reverse_lazy('Admin_panel:media')

class Update(AdminRequiredMixin, ModuleActiveRequiredMixin,UpdateView):
    template_name = 'admin_panel/module/media/edit.html'
    model = Media
    module_name = "media"
    form_class = MediaForm
    success_url = reverse_lazy('Admin_panel:media')

class Query(AdminRequiredMixin,ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/media/index.html'
    paginate_by = 15
    module_name = "media"
    model = Media
    context_object_name = 'media'
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
    model = Media
    module_name = "media"
    success_url = reverse_lazy('Admin_panel:media')
    def get(self, request, pk, *args, **kwargs):
        item = get_object_or_404(self.model, pk=pk)
        item.toggle_status()
        if item.status == 'active':
            messages.success(
                request,
                f"رسانه {item.title}' فعال شد.",
            )
        else:
            messages.warning(
                request,
                f"رسانه '{item.title}' غیرفعال شد.",
            )

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(self.success_url)

class Delete(AdminRequiredMixin,ModuleActiveRequiredMixin, DeleteView):
    model = Media
    module_name = "media"
    success_url = reverse_lazy('Admin_panel:media')