from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.conf import settings
from Admin_panel.helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin,SuperAdminMixin
from Admin_panel.mixin.module import ModuleActiveRequiredMixin
from Admin_panel.forms.FilterActive import FilterForm
from Admin_panel.forms.Module.MenuBuilder import MenuBuilderForm , LinkForm
from module.models.MenuBuilder import Menu, Menu_Links
from django.core.cache import cache

class Index(AdminRequiredMixin,ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/menu_builder/index.html'
    paginate_by = 15
    module_name = "Menu_Builder"
    model = Menu
    context_object_name = 'menus'
    form_class = FilterForm

    def get_queryset(self):
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang not in available_langs:
            lang = 'fa'
        queryset = super().get_queryset().filter(lang=lang).order_by('id')
        if not queryset.exists():
            self._seed_default_records(lang=lang)
            queryset = super().get_queryset().filter(lang=lang).order_by('id')

        return queryset

    def _seed_default_records(self, lang):
        defaults = {
            'fa': [
                {'title': 'هدر', 'name': 'header'},
                {'title': 'فوتر', 'name': 'footer'},
            ],
            'en': [
                {'title': 'header', 'name': 'header'},
                {'title': 'footer', 'name': 'footer'},
            ]
        }

        for data in defaults[lang]:
            self.model.objects.get_or_create(
                name=data['name'],
                lang=lang,
                defaults={
                    'title': data['title']
                }
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class()
        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context

class Create(SuperAdminMixin,ModuleActiveRequiredMixin,CreateView):
    template_name = 'admin_panel/module/menu_builder/create.html'
    model = Menu
    module_name = "Menu_Builder"
    form_class = MenuBuilderForm
    success_url = reverse_lazy('Admin_panel:menu')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

class Update(AdminRequiredMixin,ModuleActiveRequiredMixin, UpdateView):
    template_name = 'admin_panel/module/menu_builder/edit.html'
    model = Menu
    module_name = "Menu_Builder"
    form_class = MenuBuilderForm
    success_url = reverse_lazy('Admin_panel:menu')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

class Query(AdminRequiredMixin, ModuleActiveRequiredMixin,ListView):
    template_name = 'admin_panel/module/menu_builder/index.html'
    paginate_by = 15
    model = Menu
    module_name = "Menu_Builder"
    context_object_name = 'menus'
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


class Active(AdminRequiredMixin,ModuleActiveRequiredMixin,View):
    model = Menu
    module_name = "Menu_Builder"
    success_url = reverse_lazy('Admin_panel:menu')
    def get(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=pk)
        obj.toggle_status()
        if obj.status == 'active':
            messages.success(
                request,
                _("Menu '%(title)s' has been activated.") % {'title': item.title},
            )
        else:
            messages.warning(
                request,
                _("Menu '%(title)s' has been deactivated.") % {'title': item.title},
            )

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(self.success_url)

class Delete(SuperAdminMixin,ModuleActiveRequiredMixin, DeleteView):
    model = Menu
    module_name = "Menu_Builder"
    success_url = reverse_lazy('Admin_panel:menu')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        menu_name = self.object.name
        response = super().delete(request, *args, **kwargs)
        return response



class IndexLink(AdminRequiredMixin, ModuleActiveRequiredMixin,ListView):
    template_name = 'admin_panel/module/menu_builder/link/index.html'
    model = Menu_Links
    module_name = "Menu_Builder"
    context_object_name = 'links'

    def dispatch(self, request, *args, **kwargs):
        self.menu_obj = get_object_or_404(Menu, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (super().get_queryset()
                .filter(Menu=self.menu_obj)
                .select_related('parent')
                .order_by('order'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_obj'] = self.menu_obj
        return context


class CreateLink(AdminRequiredMixin,ModuleActiveRequiredMixin,CreateView):
    template_name = 'admin_panel/module/menu_builder/link/create.html'
    model = Menu_Links
    module_name = "Menu_Builder"
    form_class = LinkForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.menu = get_object_or_404(Menu, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_obj'] = self.menu
        return context

    def form_valid(self, form):
        form.instance.Menu = self.menu
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse('Admin_panel:menu-link', args=[self.menu.id])

class UpdateLink(AdminRequiredMixin,ModuleActiveRequiredMixin, UpdateView):
    template_name = 'admin_panel/module/menu_builder/link/edit.html'
    model = Menu_Links
    module_name = "Menu_Builder"
    form_class = LinkForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.menu = get_object_or_404(Menu, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Menu_Links, pk=self.kwargs['link_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_obj'] = self.menu
        context['link_obj'] = self.object
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse('Admin_panel:menu-link', args=[self.object.Menu.id])


class ActiveLink(AdminRequiredMixin,ModuleActiveRequiredMixin, View):
    model = Menu_Links
    module_name = "Menu_Builder"

    def get(self, request, pk, link_pk, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=link_pk, Menu_id=pk)
        obj.toggle_status()
        if obj.status == 'active':
            messages.success(
                request,
                _("Link '%(title)s' has been activated.") % {'title': item.title},
            )
        else:
            messages.warning(
                request,
                _("Link '%(title)s' has been deactivated.") % {'title': item.title},
            )

        return redirect('Admin_panel:menu-link', pk=pk)


class DeleteLink(AdminRequiredMixin,ModuleActiveRequiredMixin, DeleteView):
    model = Menu_Links
    pk_url_kwarg = 'link_pk'
    module_name = "Menu_Builder"

    def get_queryset(self):
        return super().get_queryset().filter(Menu_id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return response

    def get_success_url(self):
        return reverse('Admin_panel:menu-link', kwargs={'pk': self.kwargs['pk']})


class ChangeFieldOrder(AdminRequiredMixin, ModuleActiveRequiredMixin, View):
    module_name = "Menu_Builder"

    def get(self, request, pk, link_pk, direction):
        obj = get_object_or_404(Menu_Links.objects.select_related('Menu'), pk=link_pk, Menu_id=pk)

        with transaction.atomic():
            if direction == 'up':
                target = (
                    Menu_Links.objects
                    .filter(Menu_id=pk, order__lt=obj.order)
                    .order_by('-order')
                    .first()
                )
            else:
                target = (
                    Menu_Links.objects
                    .filter(Menu_id=pk, order__gt=obj.order)
                    .order_by('order')
                    .first()
                )

            if target:
                old_order = obj.order
                obj.order = target.order
                target.order = old_order

                obj.save(update_fields=["order"])
                target.save(update_fields=["order"])

        return redirect('Admin_panel:menu-link', pk=pk)

