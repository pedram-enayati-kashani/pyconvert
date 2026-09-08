from django.core.cache import cache
from django.shortcuts import redirect
from module.models.RedirectRuleModel import RedirectRule


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        cache_key = f"redirect_rule:{path}"

        rule_data = cache.get(cache_key)

        if rule_data is None:
            rule = RedirectRule.objects.filter(old_url=path).first()

            if rule:
                rule_data = {
                    "new_url": rule.new_url,
                    "is_permanent": rule.is_permanent,
                }
            else:
                rule_data = False

            cache.set(cache_key, rule_data, 60 * 10)

        if rule_data:
            return redirect(
                rule_data["new_url"],
                permanent=rule_data["is_permanent"],
            )

        return self.get_response(request)
