from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from Admin_panel.helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin,SuperAdminMixin
from Admin_panel.mixin.module import ModuleActiveRequiredMixin
from Admin_panel.forms.Module.Real_Estate import SellBuyForm, RentForm, FilterSellBuyForm, FilterRentForm
from module.models.Real_EstateModel import SellBuy, Rent


class Index(AdminRequiredMixin, ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/RealEstate/index.html'
    module_name = "Real_Estate"
    model = SellBuy

    def get_queryset(self):
        return SellBuy.objects.all().order_by('-created_at')[:15]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rent_list'] = Rent.objects.all().order_by('-created_at')[:15]
        context['sell_buy_list'] = context['object_list']
        return context

class SellIndex(AdminRequiredMixin, ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/RealEstate/SellBuy/index.html'
    module_name = "Real_Estate"
    model = SellBuy
    form_class = FilterSellBuyForm
    paginate_by = 15
    context_object_name = 'sell_buy_list'

    def get_queryset(self):
        return SellBuy.objects.all().order_by('-created_at')[:15]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class()
        context['rent_list'] = Rent.objects.all().order_by('-created_at')[:15]
        context['sell_buy_list'] = context['object_list']
        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context

class SellUpdate(AdminRequiredMixin,ModuleActiveRequiredMixin, UpdateView):
    template_name = 'admin_panel/module/RealEstate/SellBuy/edit.html'
    model = SellBuy
    module_name = "Real_Estate"
    form_class = SellBuyForm
    success_url = reverse_lazy('Admin_panel:real-estate-sell-buy')

class SellShow(AdminRequiredMixin,ModuleActiveRequiredMixin, DetailView):
    template_name = 'admin_panel/module/RealEstate/SellBuy/show.html'
    model = SellBuy
    module_name = "Real_Estate"
    context_object_name = 'sell_buy'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.saw != 'see':
            obj.saw = 'see'
            obj.save(update_fields=['saw'])
        return obj


class SellQuery(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/module/RealEstate/SellBuy/index.html'
    paginate_by = 15
    module_name = "Real_Estate"
    model = SellBuy
    form_class = FilterSellBuyForm
    context_object_name = 'sell_buy_list'

    def get_queryset(self):
        self.form = self.form_class(self.request.GET or None)
        queryset = SellBuy.objects.all().order_by('-id')

        if self.form.is_valid():
            type_filter = self.form.cleaned_data.get('type')
            address_filter = self.form.cleaned_data.get('address')

            if type_filter == 'buyer' or type_filter == 'seller':
                queryset = queryset.filter(type=type_filter)
            elif type_filter == 'discharge':
                queryset = queryset.filter(discharge_unit='discharge')

            if address_filter:
                queryset = queryset.filter(address__icontains=address_filter)

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


class SellDelete(AdminRequiredMixin,ModuleActiveRequiredMixin, DeleteView):
    model = SellBuy
    module_name = "Real_Estate"
    success_url = reverse_lazy('Admin_panel:real-estate-sell-buy')


class RentIndex(AdminRequiredMixin, ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/RealEstate/Rent/index.html'
    module_name = "Real_Estate"
    model = Rent
    form_class = FilterRentForm
    paginate_by = 15
    context_object_name = 'rent_list'

    def get_queryset(self):
        return SellBuy.objects.all().order_by('-created_at')[:15]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class()
        context['rent_list'] = Rent.objects.all().order_by('-created_at')[:15]
        context['sell_buy_list'] = context['object_list']
        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context

class RentUpdate(AdminRequiredMixin,ModuleActiveRequiredMixin, UpdateView):
    template_name = 'admin_panel/module/RealEstate/Rent/edit.html'
    model = Rent
    module_name = "Real_Estate"
    form_class = RentForm
    success_url = reverse_lazy('Admin_panel:real-estate-rent')

class RentShow(AdminRequiredMixin,ModuleActiveRequiredMixin, DetailView):
    template_name = 'admin_panel/module/RealEstate/Rent/show.html'
    model = Rent
    module_name = "Real_Estate"
    context_object_name = 'rent'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.saw != 'see':
            obj.saw = 'see'
            obj.save(update_fields=['saw'])
        return obj


class RentQuery(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/module/RealEstate/Rent/index.html'
    paginate_by = 15
    module_name = "Real_Estate"
    model = Rent
    form_class = FilterRentForm
    context_object_name = 'rent_list'

    def get_queryset(self):
        self.form = self.form_class(self.request.GET or None)
        queryset = Rent.objects.all().order_by('-id')

        if self.form.is_valid():
            type_filter = self.form.cleaned_data.get('type')
            address_filter = self.form.cleaned_data.get('address')

            if type_filter in ('lessor', 'tenant'):
                queryset = queryset.filter(type=type_filter)
            elif type_filter == 'discharge':
                queryset = queryset.filter(discharge_unit='discharge')

            if address_filter:
                queryset = queryset.filter(address__icontains=address_filter)

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



class RentDelete(AdminRequiredMixin,ModuleActiveRequiredMixin, DeleteView):
    model = Rent
    module_name = "Real_Estate"
    success_url = reverse_lazy('Admin_panel:real-estate-rent')