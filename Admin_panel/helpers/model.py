from django.utils.text import slugify


def generate_unique_slug(Model, text, instance_id=None):
    if not text:
        return ""

    base_slug = slugify(text, allow_unicode=True)

    if not base_slug:
        base_slug = "n-a"

    slug = base_slug
    counter = 1

    qs = Model.objects.all()

    if instance_id and instance_id != "None":
        qs = qs.exclude(pk=instance_id)

    while qs.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug
