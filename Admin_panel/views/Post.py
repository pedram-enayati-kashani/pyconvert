from django.shortcuts import redirect, get_object_or_404, HttpResponseRedirect
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from django.views.generic.list import ListView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count
from django.template.loader import render_to_string
from ..forms.Post import PostForm, PostGalleryFormSet
from ..forms.Filter import FilterForm
from ..helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin, AdminOrAuthorRequiredMixin
from App_panel.models import Post
from App_panel.models.Modules import Modules as app_modules
from Admin_panel.helpers.client.most_visited import get_posts_total_views


class Index(AdminOrAuthorRequiredMixin, ListView):
    template_name = 'admin_panel/posts/index.html'
    paginate_by = 15
    model = Post
    context_object_name = 'posts'
    form_class = FilterForm

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(comments_count=Count('comments', distinct=True))
            .order_by('-id')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class()

        posts = context.get('posts')
        post_ids = [post.id for post in posts]
        views_map = get_posts_total_views(post_ids)

        for post in posts:
            post.views_count = views_map.get(post.id, 0)

        if 'paginator' in context and 'page_obj' in context:
            context['visible_page_numbers'] = get_visible_page_numbers(
                paginator=context['paginator'],
                page_obj=context['page_obj']
            )

        return context


class Show(AdminOrAuthorRequiredMixin, DetailView):
    model = Post
    template_name = 'admin_panel/posts/show.html'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('user').prefetch_related('categories', 'tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        views_map = get_posts_total_views([post.id])
        post.views_count = views_map.get(post.id, 0)

        return context


class Create(AdminOrAuthorRequiredMixin, CreateView):
    template_name = 'admin_panel/posts/create.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('Admin_panel:post')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_builder_models(self):
        form_builder = app_modules.objects.filter(
            name='form_builder',
            status='active',
        ).first()

        if form_builder:
            from module.models.FormBuilder import (
                Form,
                PostFormAssignment,
                FormField,
                FieldValue,
            )
            return Form, PostFormAssignment, FormField, FieldValue

        return None, None, None, None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['gallery_formset'] = PostGalleryFormSet(
                self.request.POST,
                self.request.FILES,
                prefix='gallery_items',
            )
        else:
            context['gallery_formset'] = PostGalleryFormSet(
                prefix='gallery_items',
            )

        FormModel, _, _, _ = self.get_form_builder_models()

        context['available_forms'] = (
            FormModel.objects.filter(
                target_post_type='post',
                status='active',
            )
            if FormModel else []
        )

        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        gallery_formset = PostGalleryFormSet(
            request.POST,
            request.FILES,
            prefix='gallery_items',
        )

        form_id = request.POST.get('selected_form')
        _, _, Field, _ = self.get_form_builder_models()

        dynamic_errors = []

        if form_id and Field:
            dynamic_fields = Field.objects.filter(
                form_id=form_id,
                status='active',
            )

            for field in dynamic_fields:
                value = request.POST.get(f'field_{field.id}', '').strip()

                if field.required and not value:
                    dynamic_errors.append(
                        f"فیلد «{field.label}» الزامی است."
                    )
                    continue

                if not value:
                    continue

                try:
                    if field.field_type == 'email':
                        validate_email(value)

                    elif field.field_type == 'number':
                        if not value.lstrip('-').replace('.', '', 1).isdigit():
                            raise ValidationError(
                                'لطفاً یک عدد معتبر وارد کنید.'
                            )

                except ValidationError as error:
                    message = getattr(
                        error,
                        'message',
                        'مقدار واردشده معتبر نیست.',
                    )
                    dynamic_errors.append(
                        f'خطا در «{field.label}»: {message}'
                    )

        if form.is_valid() and gallery_formset.is_valid() and not dynamic_errors:
            return self.form_valid(form, gallery_formset)

        for error in dynamic_errors:
            form.add_error(None, error)

        return self.form_invalid(form)

    def form_valid(self, form, gallery_formset=None):
        with transaction.atomic():
            self.object = form.save()

            if gallery_formset:
                gallery_formset.instance = self.object
                gallery_formset.save()

            form_id = self.request.POST.get('selected_form')
            _, Assignment, Field, Value = self.get_form_builder_models()

            if form_id and Assignment and Field and Value:
                # اتصال فرم انتخاب‌شده به پست
                Assignment.objects.update_or_create(
                    post=self.object,
                    defaults={'form_id': form_id},
                )

                # ذخیره مقدار فیلدهای کاستوم مستقیم برای پست
                fields = Field.objects.filter(
                    form_id=form_id,
                    status='active',
                )

                for field in fields:
                    value = self.request.POST.get(
                        f'field_{field.id}',
                        '',
                    ).strip()

                    # فقط مقدارهای غیرخالی ذخیره می‌شوند
                    if value:
                        Value.objects.update_or_create(
                            post=self.object,
                            field=field,
                            defaults={'value': value},
                        )

        return HttpResponseRedirect(self.get_success_url())

class Update(AdminOrAuthorRequiredMixin, UpdateView):
    template_name = 'admin_panel/posts/edit.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('Admin_panel:post')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_builder_models(self):
        form_builder = app_modules.objects.filter(
            name='form_builder',
            status='active',
        ).first()

        if form_builder:
            from module.models.FormBuilder import (
                Form,
                PostFormAssignment,
                FormField,
                FieldValue,
            )
            return Form, PostFormAssignment, FormField, FieldValue

        return None, None, None, None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['gallery_formset'] = PostGalleryFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
                prefix='gallery_items',
            )
        else:
            context['gallery_formset'] = PostGalleryFormSet(
                instance=self.object,
                prefix='gallery_items',
            )

        FormModel, Assignment, Field, Value = self.get_form_builder_models()

        context['selected_form_id'] = None
        context['current_fields'] = []
        context['form_values'] = {}
        context['can_change_form'] = True

        context['available_forms'] = (
            FormModel.objects.filter(
                target_post_type='post',
                status='active',
            )
            if FormModel else []
        )

        if FormModel and Assignment and Field and Value and self.object:
            assignment = (
                Assignment.objects
                .filter(post=self.object)
                .select_related('form')
                .first()
            )

            if assignment:
                context['selected_form_id'] = assignment.form_id
                context['can_change_form'] = False

                context['current_fields'] = Field.objects.filter(
                    form_id=assignment.form_id,
                    status='active',
                ).order_by('order', 'id')

                # مقدارهای فیلدهای همین پست
                context['form_values'] = {
                    item.field_id: item.value
                    for item in Value.objects.filter(
                        post_id=self.object.pk,
                        field__form_id=assignment.form_id,
                    )
                }

        if hasattr(self, 'dynamic_errors_dict'):
            context['dynamic_errors'] = self.dynamic_errors_dict

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        gallery_formset = PostGalleryFormSet(
            request.POST,
            request.FILES,
            instance=self.object,
            prefix='gallery_items',
        )

        self.dynamic_errors_dict = {}
        form_id = request.POST.get('selected_form')
        _, _, Field, _ = self.get_form_builder_models()

        if form_id and Field:
            fields = Field.objects.filter(
                form_id=form_id,
                status='active',
            )

            for field in fields:
                value = request.POST.get(f'field_{field.id}', '').strip()

                if field.required and not value:
                    self.dynamic_errors_dict[field.id] = (
                        f"فیلد «{field.label}» الزامی است."
                    )
                    continue

                if not value:
                    continue

                try:
                    if field.field_type == 'email':
                        validate_email(value)

                    elif field.field_type == 'number':
                        if not value.lstrip('-').replace('.', '', 1).isdigit():
                            raise ValidationError(
                                'لطفاً یک عدد معتبر وارد کنید.'
                            )

                except ValidationError as error:
                    self.dynamic_errors_dict[field.id] = getattr(
                        error,
                        'message',
                        str(error),
                    )

        if form.is_valid() and gallery_formset.is_valid() and not self.dynamic_errors_dict:
            return self.form_valid(form, gallery_formset)

        return self.form_invalid(form, gallery_formset=gallery_formset)

    def form_valid(self, form, gallery_formset=None):
        with transaction.atomic():
            self.object = form.save()

            if gallery_formset:
                gallery_formset.instance = self.object
                gallery_formset.save()

            form_id = self.request.POST.get('selected_form')
            _, Assignment, Field, Value = self.get_form_builder_models()

            if form_id and Assignment and Field and Value:
                Assignment.objects.update_or_create(
                    post=self.object,
                    defaults={'form_id': form_id},
                )

                fields = Field.objects.filter(
                    form_id=form_id,
                    status='active',
                )

                for field in fields:
                    value = self.request.POST.get(
                        f'field_{field.id}',
                        '',
                    ).strip()

                    if value:
                        # ایجاد یا ویرایش مقدار فیلد برای همین پست
                        Value.objects.update_or_create(
                            post=self.object,
                            field=field,
                            defaults={'value': value},
                        )
                    else:
                        # اگر ادمین مقدار را پاک کرد، مقدار دیتابیس هم حذف شود
                        Value.objects.filter(
                            post=self.object,
                            field=field,
                        ).delete()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, gallery_formset=None):
        context = self.get_context_data(form=form)

        context['gallery_formset'] = (
            gallery_formset
            or context.get('gallery_formset')
        )

        return self.render_to_response(context)



class Query(AdminOrAuthorRequiredMixin, ListView):
    template_name = 'admin_panel/posts/index.html'
    paginate_by = 15
    model = Post
    context_object_name = 'posts'
    form_class = FilterForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        queryset = super().get_queryset()

        if self.form.is_valid():
            status_filter = self.form.cleaned_data.get('status', 'all')
            title_filter = self.form.cleaned_data.get('title', '').strip()

            if status_filter != 'all':
                queryset = queryset.filter(status=status_filter)

            if title_filter:
                queryset = queryset.filter(title__icontains=title_filter)

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
    model = Post
    success_url = reverse_lazy('Admin_panel:post')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)


class GetFormFieldsView(AdminRequiredMixin, View):
    def get(self, request, form_id):
        form_builder = app_modules.objects.filter(name="form_builder", status='active').first()
        html = ''
        if form_builder:
            from module.models.FormBuilder import Form
            form_obj = get_object_or_404(Form, pk=form_id)
            fields = form_obj.fields.filter(status='active').order_by('order')
            html = render_to_string('admin_panel/posts/_dynamic_fields.html', {
                'fields': fields,
                'values': {},
                'dynamic_errors': {}
            }, request=request)

        return JsonResponse({'html': html})
