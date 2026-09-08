from datetime import timedelta
from django.views import View
from Admin_panel.helpers.Auth import RegisterFail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpRequest
from django.contrib.auth import login, logout, authenticate
from Admin_panel.forms.Auth import LoginForm

# Auth
class LoginView(View):
    MAX_LOGIN_ATTEMPTS = 3
    LOCKOUT_TIME = 180  # 3 دقیقه

    def get(self, request):
        return render(request, 'App_panel/auth/login.html', {
            'login_form': LoginForm()
        })

    def post(self, request: HttpRequest):
        form = LoginForm(request.POST)
        rate_limiter = RegisterFail(request, self.LOCKOUT_TIME, self.MAX_LOGIN_ATTEMPTS)

        error = rate_limiter.check()
        if error:
            form.add_error(
                None,
                f'حساب موقتاً قفل شده است. {error.minutes} دقیقه و {error.seconds} ثانیه دیگر تلاش کنید.'
            )
            return render(request, 'App_panel/auth/login.html', {'login_form': form})

        if not form.is_valid():
            rate_limiter.fail_increase()
            form.add_error(None, 'نام کاربری یا کلمه عبور اشتباه است.')
            return render(request, 'App_panel/auth/login.html', {'login_form': form})

        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )

        if not user or not user.is_active or not user.is_staff:
            rate_limiter.fail_increase()
            form.add_error(None, 'نام کاربری یا کلمه عبور اشتباه است.')
            return render(request, 'App_panel/auth/login.html', {'login_form': form})

        # ✅ موفقیت
        rate_limiter.delete()
        login(request, user)

        if form.cleaned_data.get("remember_me"):
            request.session.set_expiry(timedelta(weeks=2))
        else:
            request.session.set_expiry(0)

        return redirect('App_panel:dashboard')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('Client:home')