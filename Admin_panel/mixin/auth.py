from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.http import Http404

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return (user.is_authenticated and user.is_staff and user.groups.filter(name='admin').exists())

    def handle_no_permission(self):
        raise Http404

class AdminOrAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return (user.is_authenticated and user.is_staff and user.groups.filter(name__in=['admin', 'author']).exists())

    def handle_no_permission(self):
        raise Http404

class SuperAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True

    def handle_no_permission(self):
        raise Http404
