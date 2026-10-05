from django.urls import path
from Admin_panel.views.Modules import watermark

urlpatterns = [
    path('', watermark.Index.as_view(), name='watermark'),
    path('create', watermark.Create.as_view(), name='watermark-create'),
    path('update', watermark.Update.as_view(), name='watermark-update'),
    path('active/<int:pk>', watermark.Active.as_view(), name='watermark-active'),
    path('delete/<int:pk>', watermark.Delete.as_view(), name='watermark-delete'),
]