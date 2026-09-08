from django.urls import path, include
from App_panel.views.Panel import Panel

app_name = "App_panel"
urlpatterns = [
    path('', Panel.as_view(), name='dashboard'),
    path('', include("App_panel.urls_list.Auth")),
    path('group/', include("App_panel.urls_list.Group")),
    path('table/', include("App_panel.urls_list.Table")),
    path('module/', include("App_panel.urls_list.module")),
    path('setting/', include("App_panel.urls_list.Setting")),
]
