from django.urls import path
from Admin_panel.views import Tag

urlpatterns = [
    path('', Tag.Index.as_view(), name='tag'),
    path('create', Tag.Create.as_view(), name='tag-create'),
    path('update/<int:pk>/', Tag.Update.as_view(), name='tag-update'),
    path('delete/<int:pk>',Tag.Delete.as_view(), name='tag-delete'),
    path('filter/', Tag.Query.as_view(), name='tag-query'),
]