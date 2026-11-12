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
from Admin_panel.forms.Module.socialMedia import SocialMediaForm
from module.models.SocialMediaModel import SocialMedia

class Index(AdminRequiredMixin,ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/socialMedia/index.html'
    paginate_by = 15
    module_name = "social_media"
    model = SocialMedia
    context_object_name = 'social_media'
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


    def _seed_default_records(self,lang):
        defaults = {
            'fa':[{'title': 'اینستاگرام','name':'instagram'},{'title': 'تلگرام','name': 'telegram'},
                {'title': 'واتساپ','name': 'whatsapp'},{'title': 'x','name': 'x'},
                {'title': 'ایتا','name': 'eitta'},{'title': 'روبیکا','name': 'rubika'},
                {'title': 'بله','name': 'bale'},{'title': 'سروش','name': 'soroush'}],
            'en':[{'title': 'instagram','name':'instagram'},{'title': 'telegram','name': 'telegram'},
                {'title': 'whatsapp','name': 'whatsapp'},{'title': 'x','name': 'x'}]
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
    template_name = 'admin_panel/module/socialMedia/create.html'
    model = SocialMedia
    module_name = "social_media"
    form_class = SocialMediaForm
    success_url = reverse_lazy('Admin_panel:social-media')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

class Update(AdminRequiredMixin, ModuleActiveRequiredMixin,UpdateView):
    template_name = 'admin_panel/module/socialMedia/edit.html'
    model = SocialMedia
    module_name = "social_media"
    form_class = SocialMediaForm
    success_url = reverse_lazy('Admin_panel:social-media')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

class Query(AdminRequiredMixin,ModuleActiveRequiredMixin, ListView):
    template_name = 'admin_panel/module/socialMedia/index.html'
    paginate_by = 15
    module_name = "social_media"
    model = SocialMedia
    context_object_name = 'social_media'
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
    model = SocialMedia
    module_name = "social_media"
    success_url = reverse_lazy('Admin_panel:social-media')
    def get(self, request, pk, *args, **kwargs):
        page = get_object_or_404(self.model, pk=pk)
        page.toggle_status()
        if page.status == 'active':
            messages.success(
                request,
                _("Social network '%(title)s' has been activated.") % {'title': page.title},
            )
        else:
            messages.warning(
                request,
                _("Social network '%(title)s' has been deactivated.") % {'title': page.title},
            )

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(self.success_url)

class Delete(SuperAdminMixin,ModuleActiveRequiredMixin, DeleteView):
    model = SocialMedia
    module_name = "social_media"
    success_url = reverse_lazy('Admin_panel:social-media')