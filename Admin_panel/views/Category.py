from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from ..forms.Category import CategoryForm
from ..forms.Filter import FilterForm
from ..helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin, AdminOrAuthorRequiredMixin
from App_panel.models import Category


class Index(AdminOrAuthorRequiredMixin, ListView):
    template_name = 'admin_panel/categories/index.html'
    paginate_by = 15
    model = Category
    context_object_name = 'categories'
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

class Create(AdminOrAuthorRequiredMixin,CreateView):
    template_name = 'admin_panel/categories/create.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('Admin_panel:category')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class Update(AdminOrAuthorRequiredMixin, UpdateView):
    template_name = 'admin_panel/categories/edit.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('Admin_panel:category')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class Query(AdminOrAuthorRequiredMixin, ListView):
    template_name = 'admin_panel/categories/index.html'
    paginate_by = 15
    model = Category
    context_object_name = 'categories'
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

class Delete(AdminRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('Admin_panel:category')
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)