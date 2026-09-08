from django.urls import path
from Admin_panel.views import Category

urlpatterns = [
    path('', Category.Index.as_view(), name='category'),
    path('create', Category.Create.as_view(), name='category-create'),
    path('update/<int:pk>/', Category.Update.as_view(), name='category-update'),
    path('delete/<int:pk>',Category.Delete.as_view(), name='category-delete'),
    path('filter/', Category.Query.as_view(), name='category-query'),
]