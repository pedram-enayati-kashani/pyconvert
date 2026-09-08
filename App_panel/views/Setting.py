from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, UpdateView, CreateView
from django.contrib import messages
from django.contrib.sites.models import Site
from django.urls import reverse_lazy
from App_panel.mixin.Panel_auth import AppPanelRequiredMixin
from App_panel.models.SiteInfoModel import SiteInfo
from App_panel.models.EmailModel import EmailSettings
from App_panel.forms.SiteInfo import SiteInfoForm
from App_panel.forms.Email import EmailSettingsForm
from Admin_panel.helpers.Email_Config import send_Email_test_connect

class Index(AppPanelRequiredMixin, TemplateView):
    template_name = 'App_panel/setting/index.html'
    model =SiteInfo
    context_object_name = 'setting'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = SiteInfo.objects.filter(id=1).first()
        context['site'] = Site.objects.get(id=1)
        context['email'] = EmailSettings.objects.filter(id=1).first()
        return context

class Create(AppPanelRequiredMixin,CreateView):
    template_name = 'App_panel/setting/site/create.html'
    model = SiteInfo
    form_class = SiteInfoForm
    success_url = reverse_lazy('App_panel:setting')


class Update(AppPanelRequiredMixin, UpdateView):
    template_name = 'App_panel/setting/site/edit.html'
    model = SiteInfo
    form_class = SiteInfoForm
    success_url = reverse_lazy('App_panel:setting')
    context_object_name = 'setting'

    def get_object(self, queryset=None):
        return SiteInfo.objects.filter(id=1).first()

class Active(AppPanelRequiredMixin, View):
    model = SiteInfo
    success_url = reverse_lazy('App_panel:setting')
    def get(self, request, *args, **kwargs):
        setting = get_object_or_404(self.model, id=1)
        setting.toggle_status()
        if setting.status == 'active':
            messages.success(
                request,
                f"تنظیمات '{setting.title}' فعال شد."
            )
        else:
            messages.warning(
                request,
                f"تنظیمات '{setting.title}' غیرفعال شد."
            )
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)

        return redirect(self.success_url)

class Maintenance(AppPanelRequiredMixin, View):
    model = SiteInfo
    success_url = reverse_lazy('App_panel:setting')
    def get(self, request, *args, **kwargs):
        setting = get_object_or_404(self.model, id=1)
        setting.toggle_maintenance()
        if setting.maintenance == 'active':
            messages.success(
                request,
                f"حالت بروزرسانی ' {setting.title}' فعال شد."
            )
        else:
            messages.warning(
                request,
                f"حالت بروزرسانی  '{setting.title}' غیرفعال شد."
            )
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)

        return redirect(self.success_url)

class UpdateEmail(AppPanelRequiredMixin, UpdateView):
    model = EmailSettings
    form_class = EmailSettingsForm
    template_name = 'App_panel/setting/email/edit.html'
    success_url = reverse_lazy('App_panel:setting')

    def get_object(self, queryset=None):
        obj, created = EmailSettings.objects.get_or_create(id=1)
        return obj


class TestEmailConnection(AppPanelRequiredMixin, View):
    success_url = reverse_lazy('App_panel:setting')

    def get(self, request, *args, **kwargs):
        success, message = send_Email_test_connect(request.user.email)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return redirect(self.success_url)
