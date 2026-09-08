from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from Admin_panel.forms.Module.FormBuilder import FormBuilderForm, FieldBuilderForm
from Admin_panel.forms.FilterActive import FilterForm
from Admin_panel.helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin
from Admin_panel.mixin.module import ModuleActiveRequiredMixin
from module.models.FormBuilder import Form, FormField, FieldValue
from django.db import transaction


class Index(AdminRequiredMixin,ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/form_builder/index.html'
    paginate_by = 15
    module_name = "form_builder"
    model = Form
    context_object_name = 'forms'
    form_class = FilterForm

    def get_queryset(self):
        query = super().get_queryset().order_by('-id')
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

class Create(AdminRequiredMixin,ModuleActiveRequiredMixin,CreateView):
    template_name = 'admin_panel/module/form_builder/create.html'
    model = Form
    module_name = "form_builder"
    form_class = FormBuilderForm
    success_url = reverse_lazy('Admin_panel:form-builder')

class Update(AdminRequiredMixin,ModuleActiveRequiredMixin, UpdateView):
    template_name = 'admin_panel/module/form_builder/edit.html'
    model = Form
    module_name = "form_builder"
    form_class = FormBuilderForm
    context_object_name = 'form_obj'
    success_url = reverse_lazy('Admin_panel:form-builder')

class Active(AdminRequiredMixin,ModuleActiveRequiredMixin,View):
    model = Form
    module_name = "form_builder"
    success_url = reverse_lazy('Admin_panel:form-builder')
    def get(self, request, pk, *args, **kwargs):
        form = get_object_or_404(self.model, pk=pk)
        form.toggle_status()
        if form.status == 'active':
            messages.success(
                request,
                f"فرم '{form.title}' فعال شد.",
            )
        else:
            messages.warning(
                request,
                f"فرم '{form.title}' غیرفعال شد.",
            )

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(self.success_url)

class Query(AdminRequiredMixin, ModuleActiveRequiredMixin,ListView):
    template_name = 'admin_panel/module/form_builder/index.html'
    paginate_by = 15
    module_name = "form_builder"
    model = Form
    context_object_name = 'tags'
    form_class = FilterForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        queryset = Form.objects.filter(is_deleted=False).order_by('-id')
        if self.form.is_valid():
            status_filter = self.form.cleaned_data.get('status', 'all')
            if status_filter != 'all':
                queryset = queryset.filter(status=status_filter,is_deleted=False).order_by('-id')
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

class Delete(AdminRequiredMixin, ModuleActiveRequiredMixin,DeleteView):
    model = Form
    module_name = "form_builder"
    success_url = reverse_lazy('Admin_panel:form-builder')
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)

# Fields

class IndexField(AdminRequiredMixin, ModuleActiveRequiredMixin,ListView):
    template_name = 'admin_panel/module/form_builder/field/index.html'
    model = FormField
    module_name = "form_builder"
    context_object_name = 'fields'

    def dispatch(self, request, *args, **kwargs):
        self.form_obj = get_object_or_404(Form, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (super().get_queryset().filter(form=self.form_obj).order_by('order'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_obj'] = self.form_obj
        return context


class CreateField(AdminRequiredMixin,ModuleActiveRequiredMixin,CreateView):
    template_name = 'admin_panel/module/form_builder/field/create.html'
    model = FormField
    module_name = "form_builder"
    form_class = FieldBuilderForm

    def dispatch(self, request, *args, **kwargs):
        self.form_obj = get_object_or_404(Form, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_obj'] = self.form_obj
        return context

    def form_valid(self, form):
        form.instance.form = self.form_obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Admin_panel:form-builder-field', args=[self.form_obj.id])

class UpdateField(AdminRequiredMixin,ModuleActiveRequiredMixin, UpdateView):
    template_name = 'admin_panel/module/form_builder/field/edit.html'
    model = FormField
    module_name = "form_builder"
    form_class = FieldBuilderForm

    def dispatch(self, request, *args, **kwargs):
        self.form_obj = get_object_or_404(Form, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(FormField, pk=self.kwargs['filed_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_obj'] = self.form_obj
        context['field_obj'] = self.object
        return context

    def get_success_url(self):
        return reverse('Admin_panel:form-builder-field', args=[self.form_obj.id])


class ActiveField(AdminRequiredMixin,ModuleActiveRequiredMixin, View):
    model = FormField
    module_name = "form_builder"

    def get(self, request, pk, filed_pk, *args, **kwargs):
        field_obj = get_object_or_404(self.model, pk=filed_pk)
        field_obj.toggle_status()
        if field_obj.status == 'active':
            messages.success(request, f"فیلد '{field_obj.label}' فعال شد.")
        else:
            messages.warning(request, f"فیلد '{field_obj.label}' غیرفعال شد.")
        return redirect('Admin_panel:form-builder-field', pk=pk)

class DeleteField(AdminRequiredMixin,ModuleActiveRequiredMixin, DeleteView):
    model = FormField
    module_name = "form_builder"
    template_name = 'admin_panel/module/form_builder/field_confirm_delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(FormField, pk=self.kwargs['filed_pk'])

    def get_success_url(self):
        return reverse('Admin_panel:form-builder-field', args=[self.kwargs['pk']])

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        FieldValue.objects.filter(field_id=self.object.id).delete()
        return super().delete(request, *args, **kwargs)

class ChangeFieldOrder(AdminRequiredMixin,ModuleActiveRequiredMixin, View):
    module_name = "form_builder"
    def get(self, request, pk, filed_pk, direction):
        field = get_object_or_404(FormField, pk=filed_pk, form_id=pk)
        with transaction.atomic():
            if direction == 'up':
                target = FormField.objects.filter(form_id=pk, order__lt=field.order).order_by('-order').first()
            else:
                target = FormField.objects.filter(form_id=pk, order__gt=field.order).order_by('order').first()

            if target:
                temp_order = field.order
                field.order = target.order
                target.order = temp_order

                field.save()
                target.save()

        return redirect('Admin_panel:form-builder-field', pk=pk)


