from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import get_language
from Admin_panel.forms.Tags import TagForm
from Admin_panel.helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin,AdminOrAuthorRequiredMixin
from Admin_panel.forms.Filter import FilterForm
from App_panel.models import Tag


class Index(AdminOrAuthorRequiredMixin, ListView):
    template_name = 'admin_panel/tags/index.html'
    paginate_by = 15
    model = Tag
    context_object_name = 'tags'
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

class Create(AdminOrAuthorRequiredMixin,CreateView):
    template_name = 'admin_panel/tags/create.html'
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('Admin_panel:tag')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["request"] = self.request
        return kwargs

class Update(AdminOrAuthorRequiredMixin, UpdateView):
    template_name = 'admin_panel/tags/edit.html'
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('Admin_panel:tag')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["request"] = self.request
        return kwargs

class Query(AdminOrAuthorRequiredMixin, ListView):
    template_name = 'admin_panel/tags/index.html'
    paginate_by = 15
    model = Tag
    context_object_name = 'tags'
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
    model = Tag
    success_url = reverse_lazy('Admin_panel:tag')