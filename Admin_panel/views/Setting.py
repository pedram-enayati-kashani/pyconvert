from django.views.generic import TemplateView, UpdateView
from App_panel.models.SiteInfoModel import SiteInfo
from django.urls import reverse_lazy
from django.core.cache import cache
from django.utils.translation import get_language
from django.conf import settings
from Admin_panel.forms.SiteInfo import SiteInfoForm
from Admin_panel.mixin.auth import AdminRequiredMixin

class Index(AdminRequiredMixin, TemplateView):
    template_name = 'admin_panel/setting/index.html'
    model =SiteInfo
    context_object_name = 'setting'

    def get_context_data(self, **kwargs):
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang not in available_langs:
            lang = 'fa'
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = SiteInfo.objects.filter(lang=lang).first()
        return context


class Update(AdminRequiredMixin, UpdateView):
    template_name = 'admin_panel/setting/edit.html'
    model = SiteInfo
    form_class = SiteInfoForm
    success_url = reverse_lazy('Admin_panel:setting')
    context_object_name = 'setting'

    def get_object(self, queryset=None):
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang not in available_langs:
            lang = 'fa'
        return SiteInfo.objects.filter(lang=lang).first()

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete("site_info")
        return response
