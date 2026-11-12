from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.conf import settings
from Admin_panel.helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin,SuperAdminMixin
from Admin_panel.mixin.module import ModuleActiveRequiredMixin
from Admin_panel.forms.FilterActive import FilterForm
from Admin_panel.forms.Module.redirectRule import RedirectRuleForm
from module.models.RedirectRuleModel import RedirectRule

class Index(AdminRequiredMixin,ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/redirect/index.html'
    paginate_by = 15
    model = RedirectRule
    module_name = "redirect_rule"
    context_object_name = 'redirects'
    form_class = FilterForm

    def get_queryset(self):
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang not in available_langs:
            lang = 'fa'
        return super().get_queryset().filter(lang=lang).order_by('-id')

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
    template_name = 'admin_panel/module/redirect/create.html'
    model = RedirectRule
    module_name = "redirect_rule"
    form_class = RedirectRuleForm
    success_url = reverse_lazy('Admin_panel:redirect')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

class Update(AdminRequiredMixin, ModuleActiveRequiredMixin,UpdateView):
    template_name = 'admin_panel/module/redirect/edit.html'
    model = RedirectRule
    module_name = "redirect_rule"
    form_class = RedirectRuleForm
    success_url = reverse_lazy('Admin_panel:redirect')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

class Query(AdminRequiredMixin,ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/redirect/index.html'
    paginate_by = 15
    module_name = "redirect_rule"
    model = RedirectRule
    context_object_name = 'redirects'
    form_class = FilterForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        queryset = super().get_queryset()
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang in available_langs:
            queryset = queryset.filter(lang=lang)
        else:
            queryset = queryset.filter(lang='fa')
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
    model = RedirectRule
    module_name = "redirect_rule"
    success_url = reverse_lazy('Admin_panel:redirect')
    def get(self, request, pk, *args, **kwargs):
        item = get_object_or_404(self.model, pk=pk)
        item.toggle_status()
        if item.status == 'active':
            messages.success(
                request,
                _("URL '%(url)s' has been activated.") % {'url': item.old_url},
            )
        else:
            messages.warning(
                request,
                _("URL '%(url)s' has been deactivated.") % {'url': item.old_url},
            )

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(self.success_url)

class Delete(AdminRequiredMixin,ModuleActiveRequiredMixin, DeleteView):
    model = RedirectRule
    module_name = "redirect_rule"
    success_url = reverse_lazy('Admin_panel:redirect')