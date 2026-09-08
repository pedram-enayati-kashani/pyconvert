from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    if dictionary:
        return dictionary.get(str(key)) or dictionary.get(int(key))
    return None
