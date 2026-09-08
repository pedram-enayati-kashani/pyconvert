# views
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpRequest
from Admin_panel.mixin.auth import AdminOrAuthorRequiredMixin
from Admin_panel.forms.Profile import ProfileForm, ResetPasswordForm
from App_panel.models import Users, Post, Comments, ContactUs
from Admin_panel.helpers.client.most_visited import get_posts_total_views

class DashboardView(AdminOrAuthorRequiredMixin, TemplateView):
    template_name = 'admin_panel/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = list(Post.objects.filter(status="published"))
        post_ids = [post.id for post in posts]
        views_map = get_posts_total_views(post_ids)
        for post in posts:
            post.views_count = views_map.get(post.id, 0)
        top_posts = sorted(posts, key=lambda x: x.views_count, reverse=True)[:10]
        context['top_posts'] = top_posts
        context['comment_count'] = Comments.objects.filter(saw="not-see").count()
        context["contact_count"] = ContactUs.objects.filter(saw="not-see").count()
        return context

# profile
class Profile(AdminOrAuthorRequiredMixin, TemplateView):
    template_name = 'admin_panel/profile/index.html'

class ProfileEdit(AdminOrAuthorRequiredMixin, View):
    template_name = 'admin_panel/profile/edit.html'
    form_class = ProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user, user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('Admin_panel:profile')

        return render(request, self.template_name, {'form': form})

class ResetPasswordView(AdminOrAuthorRequiredMixin,View):
    def get(self, request: HttpRequest):
        context = {
            'form': ResetPasswordForm(),
        }
        return render(request, 'admin_panel/profile/reset-password.html', context)

    def post(self, request: HttpRequest):
        reset_pass_form = ResetPasswordForm(request.POST)
        user: Users = Users.objects.filter(username__iexact=request.user.username).first()
        if reset_pass_form.is_valid():
            if user is None or not user.is_active:
                return redirect('admin_panel:profile')
            user_old_password = reset_pass_form.cleaned_data['old_password']
            is_password_correct = user.check_password(user_old_password)
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user_pass_confirm = reset_pass_form.cleaned_data.get('confirm_password')

            if not is_password_correct:
                reset_pass_form.add_error('old_password', 'کلمه عبور قدیمی اشتباه می باشد')
                return render(request, 'admin_panel/profile/reset-password.html', {'form': reset_pass_form})

            if user_new_pass != user_pass_confirm:
                reset_pass_form.add_error('confirm_password', 'فیلد تکرار کلمه عبور با فیلد کلمه عبور متفاوت است')
                return render(request, 'admin_panel/profile/reset-password.html', {'form': reset_pass_form})

            user.set_password(user_new_pass)
            user.save()
            logout(request)
            return redirect('Admin_panel:login')
        else:
            return render(request, 'admin_panel/profile/reset-password.html', {'form': reset_pass_form})