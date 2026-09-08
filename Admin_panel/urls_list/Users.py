from django.urls import path
from Admin_panel.views import Users

urlpatterns = [
    path('', Users.Index.as_view(), name='user'),
    path('create', Users.Create.as_view(), name='user-create'),
    path('update/<int:pk>/', Users.Update.as_view(), name='user-update'),
    path('active/<int:pk>', Users.Active.as_view(), name='user-active'),
    path('delete/<int:pk>', Users.Delete.as_view(), name='user-delete'),
    path('filter/', Users.Query.as_view(), name='user-query'),
]