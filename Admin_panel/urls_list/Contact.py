from django.urls import path
from Admin_panel.views import Contact

urlpatterns = [
    path('', Contact.Index.as_view(), name='contact'),
    path('show/<int:pk>', Contact.Show.as_view(), name='contact-show'),
    path('message/<int:pk>', Contact.Reply.as_view(), name='contact-message'),
    path('delete/<int:pk>',Contact.Delete.as_view(), name='contact-delete'),
    path('filter', Contact.Query.as_view(), name='contact-query'),
]