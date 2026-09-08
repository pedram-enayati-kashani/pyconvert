from django.urls import path
from Admin_panel.views import Page

urlpatterns = [
    path('', Page.Index.as_view(), name='page'),
    path('create', Page.Create.as_view(), name='page-create'),
    path('update/<int:pk>/', Page.Update.as_view(), name='page-update'),
    path('active/<int:pk>', Page.Active.as_view(), name='page-active'),
    # path('section/delete/<int:pk>',Page.SectionActive.as_view(), name='page-delete'),
    path('filter/', Page.Query.as_view(), name='page-query'),
]