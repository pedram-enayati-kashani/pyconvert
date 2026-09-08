from django.urls import path
from App_panel.views import Setting

urlpatterns = [
    path('', Setting.Index.as_view(), name='setting'),
    path('create', Setting.Create.as_view(), name='setting-create'),
    path('update', Setting.Update.as_view(), name='setting-update'),
    path('active', Setting.Active.as_view(), name='setting-active'),
    path('maintenance', Setting.Maintenance.as_view(), name='setting-maintenance'),
    path('email-update', Setting.UpdateEmail.as_view(), name='setting-email-update'),
    path('email-test-connection', Setting.TestEmailConnection.as_view(), name='setting-email-test-connection'),
]