from django.urls import path
from Admin_panel.views.Modules import Media

urlpatterns = [
    # Form
    path('', Media.Index.as_view(), name='media'),
    path('create', Media.Create.as_view(), name='media-create'),
    path('show/<int:pk>', Media.Show.as_view(), name='media-show'),
    path('update/<int:pk>', Media.Update.as_view(), name='media-update'),
    path('active/<int:pk>', Media.Active.as_view(), name='media-active'),
    path('delete/<int:pk>', Media.Delete.as_view(), name='media-delete'),
    path('filter/', Media.Query.as_view(), name='media-query'),
]