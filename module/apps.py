from django.apps import AppConfig


class ModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module'

    def ready(self):
        import module.signals.delete_image
        import module.signals.link_update_cache
        import module.signals.cache
        import module.signals.cache_formbuilder
        import module.signals.adv_signals
        import module.signals.Redirect
        import module.signals.cache_watermark
