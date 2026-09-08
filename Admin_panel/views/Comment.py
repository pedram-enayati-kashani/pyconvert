from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from django.views.generic.list import ListView
from ..forms.Comment import CommentForm
from ..forms.FilterComment import FilterCommentForm
from ..helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin
from App_panel.models.CommentsModel import Comments


class Index(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/comments/index.html'
    paginate_by = 15
    model = Comments
    context_object_name = 'comments'
    form_class = FilterCommentForm

    def get_queryset(self):
        return super().get_queryset().select_related('post').prefetch_related('children').filter(parent=None).order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class()
        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context


class Show(AdminRequiredMixin, DetailView):
    model = Comments
    template_name = "admin_panel/comments/show.html"
    context_object_name = "comment"

    def get_queryset(self):
        return Comments.objects.select_related('user', 'post').prefetch_related('children')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.saw == 'not-see':
            obj.saw = 'see'
            obj.save(update_fields=['saw'])
        return obj

class Create(AdminRequiredMixin,CreateView):
    template_name = 'admin_panel/comments/create.html'
    model = Comments
    form_class = CommentForm
    success_url = reverse_lazy('Admin_panel:comment')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class Update(AdminRequiredMixin, UpdateView):
    template_name = 'admin_panel/comments/edit.html'
    model = Comments
    form_class = CommentForm
    success_url = reverse_lazy('Admin_panel:comment')
    context_object_name = 'comment'


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.saw == 'not-see':
            obj.saw = 'see'
            obj.save(update_fields=['saw'])
        return obj

class Query(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/comments/index.html'
    paginate_by = 15
    model = Comments
    context_object_name = 'comments'
    form_class = FilterCommentForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        queryset = super().get_queryset()
        if self.form.is_valid():
            selected_value = self.form.cleaned_data.get('status')
            if selected_value in ["not-see", "see"]:
                queryset = queryset.filter(saw=selected_value)
            elif selected_value in ["approved", "rejected", "pending"]:
                queryset = queryset.filter(status=selected_value)
        return queryset.filter(parent=None).order_by('-updated_at')

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
    model = Comments
    success_url = reverse_lazy('Admin_panel:comment')