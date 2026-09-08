from django.urls import path
from Admin_panel.views import Setting

urlpatterns = [
    path('', Setting.Index.as_view(), name='setting'),
    path('update', Setting.Update.as_view(), name='setting-update'),
]