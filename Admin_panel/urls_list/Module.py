from django.urls import path, include
from Admin_panel.views import Module
from Admin_panel.views.json_view.menu_builder import resolve_menu_target

urlpatterns = [
    path('', Module.Index.as_view(), name='module'),
    path('form-builder/', include("Admin_panel.urls_list.Module_List.FormBuilder")),
    path('social-media/', include("Admin_panel.urls_list.Module_List.socialMedia")),
    path('menu-builder/', include("Admin_panel.urls_list.Module_List.MenuBuilder")),
    path('adv-text/', include("Admin_panel.urls_list.Module_List.AdvText")),
    path('adv-image/', include("Admin_panel.urls_list.Module_List.AdvImage")),
    path('redirect-rule/', include("Admin_panel.urls_list.Module_List.redirect_rule")),
    path('watermark/', include("Admin_panel.urls_list.Module_List.watermark")),
    path('real-estate/', include("Admin_panel.urls_list.Module_List.RealEstate")),
    path('media/', include("Admin_panel.urls_list.Module_List.media")),
    path("json/resolve-menu-target/", resolve_menu_target, name="link-resolve_target"),
]