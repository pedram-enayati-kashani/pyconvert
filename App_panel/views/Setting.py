from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, UpdateView, CreateView
from django.contrib import messages
from django.contrib.sites.models import Site
from django.urls import reverse_lazy
from django.utils.translation import get_language
from django.conf import settings
from App_panel.mixin.Panel_auth import AppPanelRequiredMixin
from App_panel.models.SiteInfoModel import SiteInfo
from App_panel.models.EmailModel import EmailSettings
from App_panel.models.SMSModel import SMSSettings
from App_panel.forms.SiteInfo import SiteInfoForm
from App_panel.forms.Email import EmailSettingsForm
from App_panel.forms.sms import SmsSettingsForm
from Admin_panel.helpers.Email_Config import send_Email_test_connect

class Index(AppPanelRequiredMixin, TemplateView):
    template_name = 'App_panel/setting/index.html'
    model =SiteInfo
    context_object_name = 'setting'

    def get_context_data(self, **kwargs):
        lang = get_language()
        context = super().get_context_data(**kwargs)
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang in available_langs:
            context[self.context_object_name] = SiteInfo.objects.filter(lang=lang).first()
        context['site'] = Site.objects.get(id=1)
        return context

class Create(AppPanelRequiredMixin,CreateView):
    template_name = 'App_panel/setting/site/create.html'
    model = SiteInfo
    form_class = SiteInfoForm
    success_url = reverse_lazy('App_panel:setting')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class Update(AppPanelRequiredMixin, UpdateView):
    template_name = 'App_panel/setting/site/edit.html'
    model = SiteInfo
    form_class = SiteInfoForm
    success_url = reverse_lazy('App_panel:setting')
    context_object_name = 'setting'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_object(self, queryset=None):
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang in available_langs:
            site = SiteInfo.objects.filter(lang=lang).first()
        else:
            site = SiteInfo.objects.filter(lang="fa").first()
        return site

class Active(AppPanelRequiredMixin, View):
    model = SiteInfo
    success_url = reverse_lazy('App_panel:setting')
    def get(self, request, *args, **kwargs):
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang in available_langs:
            setting = get_object_or_404(self.model, lang=lang)
        else:
            setting = get_object_or_404(self.model, lang="fa")
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

class IndexEmail(AppPanelRequiredMixin, TemplateView):
    template_name = 'App_panel/setting/email/index.html'
    model =EmailSettings
    context_object_name = 'email'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang in available_langs:
            context[self.context_object_name] = EmailSettings.objects.filter(lang=lang).first()
        return context

class UpdateEmail(AppPanelRequiredMixin, UpdateView):
    model = EmailSettings
    form_class = EmailSettingsForm
    template_name = 'App_panel/setting/email/edit.html'
    success_url = reverse_lazy('App_panel:setting-email')

    def get_object(self, queryset=None):
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang in available_langs:
            obj, created = EmailSettings.objects.get_or_create(lang=lang)
        else:
            obj, created = EmailSettings.objects.get_or_create(lang="fa")
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


class IndexSMS(AppPanelRequiredMixin, TemplateView):
    template_name = 'App_panel/setting/sms/index.html'
    model =SMSSettings
    context_object_name = 'sms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang in available_langs:
            context[self.context_object_name] = SMSSettings.objects.filter(lang=lang).first()
        return context

class UpdateSMS(AppPanelRequiredMixin, UpdateView):
    model = SMSSettings
    form_class = SmsSettingsForm
    template_name = 'App_panel/setting/sms/edit.html'
    success_url = reverse_lazy('App_panel:setting-sms')

    def get_object(self, queryset=None):
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang in available_langs:
            obj, created = SMSSettings.objects.get_or_create(lang=lang)
        else:
            obj, created = SMSSettings.objects.get_or_create(lang="fa")
        return obj
