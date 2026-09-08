from django.http import Http404
from App_panel.models.Modules import Modules

class ModuleActiveRequiredMixin:
    module_name = None

    def dispatch(self, request, *args, **kwargs):
        if not self.module_name:
            raise ValueError("module_name must be set on the view.")

        is_active = Modules.objects.filter(
            name=self.module_name,
            status='active'
        ).exists()

        if not is_active:
            raise Http404("Module not found or inactive.")

        return super().dispatch(request, *args, **kwargs)