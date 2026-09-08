from django.urls import path
from Admin_panel.views.Modules import MenuBuilder

urlpatterns = [
    # menu
    path('', MenuBuilder.Index.as_view(), name='menu'),
    path('create', MenuBuilder.Create.as_view(), name='menu-create'),
    path('update/<int:pk>', MenuBuilder.Update.as_view(), name='menu-update'),
    path('active/<int:pk>', MenuBuilder.Active.as_view(), name='menu-active'),
    path('delete/<int:pk>', MenuBuilder.Delete.as_view(), name='menu-delete'),
    path('filter/', MenuBuilder.Query.as_view(), name='menu-query'),

    # links
    path('<int:pk>/link', MenuBuilder.IndexLink.as_view(), name='menu-link'),
    path('<int:pk>/link/create', MenuBuilder.CreateLink.as_view(), name='menu-link-create'),
    path('<int:pk>/link/update/<int:link_pk>', MenuBuilder.UpdateLink.as_view(), name='menu-link-update'),
    path('<int:pk>/link/active/<int:link_pk>', MenuBuilder.ActiveLink.as_view(), name='menu-link-active'),
    path('<int:pk>/link/delete/<int:link_pk>', MenuBuilder.DeleteLink.as_view(), name='menu-link-delete'),
    # در urls.py
    path('<int:pk>/link/to-up/<int:link_pk>', MenuBuilder.ChangeFieldOrder.as_view(), {'direction': 'up'}, name='menu-link-to-up'),
    path('<int:pk>/link/to-down/<int:link_pk>', MenuBuilder.ChangeFieldOrder.as_view(), {'direction': 'down'}, name='menu-link-to-down'),
]