from Admin_panel.mixin.auth import AdminRequiredMixin
from django.views.generic import TemplateView, UpdateView
from App_panel.models.SiteInfoModel import SiteInfo
from django.urls import reverse_lazy
from ..forms.SiteInfo import SiteInfoForm
from django.core.cache import cache

class Index(AdminRequiredMixin, TemplateView):
    template_name = 'admin_panel/setting/index.html'
    model =SiteInfo
    context_object_name = 'setting'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = SiteInfo.objects.filter(id=1).first()
        return context


class Update(AdminRequiredMixin, UpdateView):
    template_name = 'admin_panel/setting/edit.html'
    model = SiteInfo
    form_class = SiteInfoForm
    success_url = reverse_lazy('Admin_panel:setting')
    context_object_name = 'setting'

    def get_object(self, queryset=None):
        return SiteInfo.objects.filter(id=1).first()

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete("site_info")
        return response
