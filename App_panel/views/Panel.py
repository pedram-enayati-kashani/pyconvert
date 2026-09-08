from App_panel.mixin.Panel_auth import AppPanelRequiredMixin
from django.views.generic import TemplateView

class Panel(AppPanelRequiredMixin, TemplateView):
    template_name = 'App_panel/dashboard.html'

