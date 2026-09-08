from django.urls import path
from Admin_panel.views import Sections

urlpatterns = [
    path('', Sections.Index.as_view(), name='section'),
    path('create', Sections.Create.as_view(), name='section-create'),
    path('update/<int:pk>/', Sections.Update.as_view(), name='section-update'),
    path('active/<int:pk>', Sections.Active.as_view(), name='section-active'),
    path('delete/<int:pk>',Sections.Delete.as_view(), name='section-delete'),
    path('filter/', Sections.Query.as_view(), name='section-query'),
]