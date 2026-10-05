from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from Admin_panel.forms.Sections import SectionForm
from Admin_panel.forms.FilterActive import FilterForm
from Admin_panel.helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin
from App_panel.models import Section


class Index(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/sections/index.html'
    paginate_by = 15
    model = Section
    context_object_name = 'sections'
    form_class = FilterForm

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        lang = get_language()
        if lang == 'fa':
            queryset = queryset.filter(lang='fa')
        elif lang == 'en':
            queryset = queryset.filter(lang='en')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class()
        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context

class Create(AdminRequiredMixin,CreateView):
    template_name = 'admin_panel/sections/create.html'
    model = Section
    form_class = SectionForm
    success_url = reverse_lazy('Admin_panel:section')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

class Update(AdminRequiredMixin, UpdateView):
    template_name = 'admin_panel/sections/edit.html'
    model = Section
    form_class = SectionForm
    success_url = reverse_lazy('Admin_panel:section')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

class Active(AdminRequiredMixin,View):
    model = Section
    success_url = reverse_lazy('Admin_panel:section')
    def get(self, request, pk, *args, **kwargs):
        section = get_object_or_404(self.model, pk=pk)
        section.toggle_status()
        if section.status == 'active':
            messages.success(
                request,
                _("Section '%(title)s' has been activated.") % {'title': section.title},
            )
        else:
            messages.warning(
                request,
                _("Section '%(title)s' has been deactivated.") % {'title': section.title},
            )
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(self.success_url)

class Query(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/sections/index.html'
    paginate_by = 15
    model = Section
    context_object_name = 'sections'
    form_class = FilterForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        queryset = super().get_queryset()
        lang = get_language()
        if lang == 'fa':
            queryset = queryset.filter(lang='fa')
        elif lang == 'en':
            queryset = queryset.filter(lang='en')
        if self.form.is_valid():
            status_filter = self.form.cleaned_data.get('status', 'all')
            if status_filter == 'active':
                queryset = queryset.filter(status='active')
            elif status_filter == 'inactive':
                queryset = queryset.filter(status='inactive')

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

class Delete(AdminRequiredMixin, DeleteView):
    model = Section
    success_url = reverse_lazy('Admin_panel:section')
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)