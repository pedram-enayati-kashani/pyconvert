from django.urls import path
from Admin_panel.views import Post

urlpatterns = [
    path('', Post.Index.as_view(), name='post'),
    path('create', Post.Create.as_view(), name='post-create'),
    path('show/<int:pk>/', Post.Show.as_view(), name='post-show'),
    path('update/<int:pk>/', Post.Update.as_view(), name='post-update'),
    path('delete/<int:pk>',Post.Delete.as_view(), name='post-delete'),
    path('filter/', Post.Query.as_view(), name='post-query'),
    path('get-fields/<int:form_id>/', Post.GetFormFieldsView.as_view(), name='get_form_fields'),
]