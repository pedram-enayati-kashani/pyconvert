from django import template

register = template.Library()


def check_group(user, groups):

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return (
        user.is_staff and
        user.groups.filter(name__in=groups).exists()
    )


@register.filter
def is_admin(user):
    return check_group(user, ['admin'])


@register.filter
def is_author(user):
    return check_group(user, ['author'])


@register.filter
def is_admin_or_author(user):
    return check_group(user, ['admin', 'author'])

@register.filter
def is_superuser(user):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True