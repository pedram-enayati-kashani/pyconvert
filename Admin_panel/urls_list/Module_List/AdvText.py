from django.urls import path
from Admin_panel.views.Modules import AdvText

urlpatterns = [
    # Form
    path('', AdvText.Index.as_view(), name='adv-text'),
    path('create', AdvText.Create.as_view(), name='adv-text-create'),
    path('update/<int:pk>', AdvText.Update.as_view(), name='adv-text-update'),
    path('active/<int:pk>', AdvText.Active.as_view(), name='adv-text-active'),
    path('delete/<int:pk>', AdvText.Delete.as_view(), name='adv-text-delete'),
    path('filter/', AdvText.Query.as_view(), name='adv-text-query'),
]