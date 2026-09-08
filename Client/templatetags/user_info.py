from django import template

register = template.Library()

@register.filter(name="username")
def username_filter(user):
    if not user:
        return ""

    display_mode = getattr(user, "display_name", "username")

    if display_mode == "first_last":
        parts = [user.first_name, user.last_name]
        return " ".join([p for p in parts if p]) or (user.get_username() if hasattr(user, "get_username") else str(user))

    if display_mode == "last_first":
        parts = [user.last_name, user.first_name]
        return " ".join([p for p in parts if p]) or (user.get_username() if hasattr(user, "get_username") else str(user))

    # پیش‌فرض: username
    return user.get_username() if hasattr(user, "get_username") else getattr(user, "username", str(user))
