import time
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.cache import cache
from types import SimpleNamespace

UserModel = get_user_model()

class UsernameOrEmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

class RegisterFail:
    def __init__(self, request, lockout_time=180, fail_number=3):
        self.current_time = time.time()
        self.lockout_time = lockout_time
        self.fail_number = fail_number

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            self.ip = x_forwarded_for.split(',')[0].strip()
        else:
            self.ip = request.META.get('REMOTE_ADDR')

        self.count_key = f'login_failed_count_{self.ip}'
        self.lock_key = f'login_failed_lock_{self.ip}'

    def check(self):
        """بررسی قفل بودن. اگر قفل بود، آبجکت زمان برمی‌گرداند."""
        lockout_until = cache.get(self.lock_key)

        if lockout_until and self.current_time < lockout_until:
            remaining = int(lockout_until - self.current_time)
            return SimpleNamespace(
                minutes=remaining // 60,
                seconds=remaining % 60
            )
        return None

    def fail_increase(self):
        """افزایش شمارنده خطا و اعمال قفل در صورت نیاز"""
        failed_count = cache.get(self.count_key, 0)
        failed_count += 1

        # ذخیره شمارنده با TTL کمی بیشتر از زمان قفل
        cache.set(self.count_key, failed_count, self.lockout_time + 60)

        if failed_count >= self.fail_number:
            lockout_until = self.current_time + self.lockout_time
            cache.set(self.lock_key, lockout_until, self.lockout_time)

    def delete(self):
        cache.delete(self.count_key)
        cache.delete(self.lock_key)