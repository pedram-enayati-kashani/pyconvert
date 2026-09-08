from django.urls import path
from Admin_panel.views.Modules import SocialMedia

urlpatterns = [
    # Form
    path('', SocialMedia.Index.as_view(), name='social-media'),
    path('create', SocialMedia.Create.as_view(), name='social-media-create'),
    path('update/<int:pk>', SocialMedia.Update.as_view(), name='social-media-update'),
    path('active/<int:pk>', SocialMedia.Active.as_view(), name='social-media-active'),
    path('delete/<int:pk>', SocialMedia.Delete.as_view(), name='social-media-delete'),
    path('filter/', SocialMedia.Query.as_view(), name='social-media-query'),
]