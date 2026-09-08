from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from ..forms.Users import UserForm
from ..forms.FilterActive import FilterForm
from ..helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin
from App_panel.models import Users


class Index(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/users/index.html'
    paginate_by = 15
    model = Users
    context_object_name = 'users'
    form_class = FilterForm

    def get_queryset(self):
        query = super().get_queryset().exclude(id=1)
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

class Create(AdminRequiredMixin,CreateView):
    template_name = 'admin_panel/users/create.html'
    model = Users
    form_class = UserForm
    success_url = reverse_lazy('Admin_panel:user')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.is_active = True
        return super().form_valid(form)

class Update(AdminRequiredMixin, UpdateView):
    template_name = 'admin_panel/users/edit.html'
    model = Users
    context_object_name = 'userUpdate'
    form_class = UserForm
    success_url = reverse_lazy('Admin_panel:user')

class Active(AdminRequiredMixin, View):
    model = Users
    success_url = reverse_lazy('Admin_panel:user')

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(self.model, pk=pk)
        user.toggle_status()
        if user.is_active:
            messages.success(
                request,
                f"کاربر '{user.username}' فعال شد."
            )
        else:
            messages.warning(
                request,
                f"کاربر '{user.username}' غیرفعال شد."
            )
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)

        return redirect(self.success_url)

class Query(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/users/index.html'
    paginate_by = 15
    model = Users
    context_object_name = 'users'
    form_class = FilterForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        queryset = super().get_queryset().exclude(id=1)
        if self.form.is_valid():
            status_filter = self.form.cleaned_data.get('status', 'all')
            if status_filter == 'active':
                queryset = queryset.exclude(id=1).filter(is_active=True)
            elif status_filter == 'inactive':
                queryset = queryset.exclude(id=1).filter(is_active=False)

        return queryset

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
    model = Users
    success_url = reverse_lazy('Admin_panel:user')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)