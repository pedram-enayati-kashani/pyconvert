from django.urls import path
from Admin_panel.views.Modules import AdvImage

urlpatterns = [
    # Form
    path('', AdvImage.Index.as_view(), name='adv-image'),
    path('create', AdvImage.Create.as_view(), name='adv-image-create'),
    path('update/<int:pk>', AdvImage.Update.as_view(), name='adv-image-update'),
    path('active/<int:pk>', AdvImage.Active.as_view(), name='adv-image-active'),
    path('delete/<int:pk>', AdvImage.Delete.as_view(), name='adv-image-delete'),
    path('filter/', AdvImage.Query.as_view(), name='adv-image-query'),
]