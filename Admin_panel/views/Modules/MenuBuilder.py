from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.db import transaction
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
        if not self.model.objects.exists():
            self._seed_default_records()
        return super().get_queryset().order_by('id')

    def _seed_default_records(self):
        defaults = [
            {
                'title': 'هدر',
                'name':'header'
            },
            {
                'title': 'فوتر',
                'name': 'footer'
            },
        ]
        for data in defaults:
            self.model.objects.get_or_create(
                title=data['title'],
                name=data['name'],
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

class Update(AdminRequiredMixin,ModuleActiveRequiredMixin, UpdateView):
    template_name = 'admin_panel/module/menu_builder/edit.html'
    model = Menu
    module_name = "Menu_Builder"
    form_class = MenuBuilderForm
    success_url = reverse_lazy('Admin_panel:menu')

    def form_valid(self, form):
        old_name = self.get_object().name
        response = super().form_valid(form)
        new_name = self.object.name
        cache.delete(f"menu_links_cache_{old_name}")
        cache.delete(f"menu_links_cache_{new_name}")

        return response

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
        cache.delete(f"menu_links_cache_{obj.name}")
        if obj.status == 'active':
            messages.success(
                request,
                f"منو '{obj.title}' فعال شد.",
            )
        else:
            messages.warning(
                request,
                f"منو '{obj.title}' غیرفعال شد.",
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
        cache.delete(f"menu_links_cache_{menu_name}")
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
        cache.delete(f"menu_links_cache_{self.menu.name}")
        return response

    def get_success_url(self):
        return reverse('Admin_panel:menu-link', args=[self.menu.id])

class UpdateLink(AdminRequiredMixin,ModuleActiveRequiredMixin, UpdateView):
    template_name = 'admin_panel/module/menu_builder/link/edit.html'
    model = Menu_Links
    module_name = "Menu_Builder"
    form_class = LinkForm

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
        old_menu = self.get_object().Menu
        response = super().form_valid(form)
        new_menu = self.object.Menu

        if old_menu:
            cache.delete(f"menu_links_cache_{old_menu.name}")
        if new_menu:
            cache.delete(f"menu_links_cache_{new_menu.name}")

        return response

    def get_success_url(self):
        return reverse('Admin_panel:menu-link', args=[self.object.Menu.id])


class ActiveLink(AdminRequiredMixin,ModuleActiveRequiredMixin, View):
    model = Menu_Links
    module_name = "Menu_Builder"

    def get(self, request, pk, link_pk, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=link_pk, Menu_id=pk)
        obj.toggle_status()
        cache.delete(f"menu_links_cache_{obj.Menu.name}")
        if obj.status == 'active':
            messages.success(request, f"لینک '{obj.title}' فعال شد.")
        else:
            messages.warning(request, f"لینک '{obj.title}' غیرفعال شد.")

        return redirect('Admin_panel:menu-link', pk=pk)


class DeleteLink(AdminRequiredMixin,ModuleActiveRequiredMixin, DeleteView):
    model = Menu_Links
    pk_url_kwarg = 'link_pk'
    module_name = "Menu_Builder"

    def get_queryset(self):
        return super().get_queryset().filter(Menu_id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        menu = self.object.Menu

        response = super().delete(request, *args, **kwargs)

        cache.delete(f"menu_links_cache_{menu.name}")
        return response

    def get_success_url(self):
        return reverse('Admin_panel:menu-link', kwargs={'pk': self.kwargs['pk']})


class ChangeFieldOrder(AdminRequiredMixin, ModuleActiveRequiredMixin, View):
    module_name = "Menu_Builder"

    def get(self, request, pk, link_pk, direction):
        obj = get_object_or_404(Menu_Links.objects.select_related('Menu'), pk=link_pk, Menu_id=pk)
        menu_name = obj.Menu.name

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

                transaction.on_commit(lambda: cache.delete(f"menu_links_cache_{menu_name}"))

        return redirect('Admin_panel:menu-link', pk=pk)



