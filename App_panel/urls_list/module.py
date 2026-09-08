from django.urls import path
from App_panel.views import Module

urlpatterns = [
    path('', Module.Index.as_view(), name='module'),
    path('create', Module.Create.as_view(), name='module-create'),
    path('update/<int:pk>/', Module.Update.as_view(), name='module-update'),
    path('active/<int:pk>', Module.Active.as_view(), name='module-active'),
    path('delete/<int:pk>',Module.Delete.as_view(), name='module-delete'),
]