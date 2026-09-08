from django.apps import AppConfig


class App_panelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App_panel'

    def ready(self):
        import App_panel.signals.site_image
        import App_panel.signals.delete_image
        import App_panel.signals.post_update_cache
        import App_panel.signals.category_signals
        import App_panel.signals.tag_signals
        import App_panel.signals.section_signals
        import App_panel.signals.user_signals
        import App_panel.signals.site
        import App_panel.signals.page