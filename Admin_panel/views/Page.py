from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from django.views.generic.list import ListView
from ..forms.Page import PageForm
from ..forms.Filter import FilterForm
from ..helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin, SuperAdminMixin
from App_panel.models import Page


class Index(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/page/index.html'
    paginate_by = 15
    model = Page
    context_object_name = 'pages'
    form_class = FilterForm

    def get_queryset(self):
        query = super().get_queryset().order_by('id')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class()
        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context

class Create(SuperAdminMixin,CreateView):
    template_name = 'admin_panel/page/create.html'
    model = Page
    form_class = PageForm
    success_url = reverse_lazy('Admin_panel:page')

class Update(AdminRequiredMixin, UpdateView):
    template_name = 'admin_panel/page/edit.html'
    model = Page
    form_class = PageForm
    success_url = reverse_lazy('Admin_panel:page')

class Active(AdminRequiredMixin,View):
    model = Page
    success_url = reverse_lazy('Admin_panel:page')
    def get(self, request, pk, *args, **kwargs):
        page = get_object_or_404(self.model, pk=pk)
        page.toggle_status()
        if page.status == 'active':
            messages.success(
                request,
                f"برچسب '{page.title}' فعال شد.",
            )
        else:
            messages.warning(
                request,
                f"برچسب '{page.title}' غیرفعال شد.",
            )

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(self.success_url)

class Query(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/page/index.html'
    paginate_by = 15
    model = Page
    context_object_name = 'pages'
    form_class = FilterForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        queryset = super().get_queryset()
        if self.form.is_valid():
            status_filter = self.form.cleaned_data.get('status', 'all')
            if status_filter == 'active':
                queryset = queryset.filter(status='active')
            elif status_filter == 'inactive':
                queryset = queryset.filter(status='inactive')

        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form

        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context