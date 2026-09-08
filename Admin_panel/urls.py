# Admin_panel/urls.py
from django.urls import path, include
from Admin_panel.views.Admin import DashboardView
from Admin_panel.views.json_view.models import get_slug

app_name = "Admin_panel"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('', include("Admin_panel.urls_list.Auth")),
    path('profile/', include("Admin_panel.urls_list.Profile")),
    path('section/', include("Admin_panel.urls_list.Section")),
    path('tag/', include("Admin_panel.urls_list.Tag")),
    path('category/', include("Admin_panel.urls_list.Category")),
    path('post/', include("Admin_panel.urls_list.Post")),
    path('page/', include("Admin_panel.urls_list.Page")),
    path('comment/', include("Admin_panel.urls_list.Comment")),
    path('user/', include("Admin_panel.urls_list.Users")),
    path('module/', include("Admin_panel.urls_list.Module")),
    path('contact/', include("Admin_panel.urls_list.Contact")),
    path('setting/', include("Admin_panel.urls_list.Setting")),
    path('slugify/', get_slug, name='get-slug')
]
