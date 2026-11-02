from django.views.generic.list import ListView
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from Admin_panel.helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin
from App_panel.models.Modules import Modules


class Index(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/module/index.html'
    paginate_by = 15
    model = Modules
    context_object_name = 'modules'

    def get_queryset(self):
        query = super().get_queryset().order_by('created_at')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for module in context['modules']:
            if module.name == "form_builder":
                module.title = _("Form Builder")
                module.detail_url = reverse('Admin_panel:form-builder')
            elif module.name == "Menu_Builder":
                module.title = _("Menu Builder")
                module.detail_url = reverse('Admin_panel:menu')
            elif module.name == "social_media":
                module.title = _("Social Media")
                module.detail_url = reverse('Admin_panel:social-media')
            elif module.name == "adv_text":
                module.title = _("Text Advertisement")
                module.detail_url = reverse('Admin_panel:adv-text')
            elif module.name == "adv_image":
                module.title = _("Banner Advertisement")
                module.detail_url = reverse('Admin_panel:adv-image')
            elif module.name == "redirect_rule":
                module.title = _("Address Redirect")
                module.detail_url = reverse('Admin_panel:redirect')
            elif module.name == "watermark":
                module.title = _("Watermark")
                module.detail_url = reverse('Admin_panel:watermark')
            elif module.name == "Real_Estate":
                module.title = _("Real Estate")
                module.detail_url = reverse('Admin_panel:real-estate')
            elif module.name == "media":
                module.title = _("Media")
                module.detail_url = reverse('Admin_panel:menu')

        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context