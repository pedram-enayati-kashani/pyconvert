from django.urls import path
from Admin_panel.views import Comment

urlpatterns = [
    path('', Comment.Index.as_view(), name='comment'),
    path('create', Comment.Create.as_view(), name='comment-create'),
    path('show/<int:pk>', Comment.Show.as_view(), name='comment-show'),
    path('update/<int:pk>/', Comment.Update.as_view(), name='comment-update'),
    path('delete/<int:pk>',Comment.Delete.as_view(), name='comment-delete'),
    path('filter/', Comment.Query.as_view(), name='comment-query'),
]