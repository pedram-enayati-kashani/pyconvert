from django.urls import path
from App_panel.views import Group

urlpatterns = [
    path('', Group.Index.as_view(), name='group'),
    path('create', Group.Create.as_view(), name='group-create'),
    path('update/<int:pk>/', Group.Update.as_view(), name='group-update'),
    path('active/<int:pk>', Group.Active.as_view(), name='group-active'),
    path('delete/<int:pk>',Group.Delete.as_view(), name='group-delete'),
]