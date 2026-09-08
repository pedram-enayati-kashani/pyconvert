from django.urls import path
from Admin_panel.views import Admin

urlpatterns = [
    path('', Admin.Profile.as_view(), name='profile'),
    path('edit',Admin.ProfileEdit.as_view(), name='profile-edit'),
    path('reset-password',Admin.ResetPasswordView.as_view(), name='reset-password'),
]