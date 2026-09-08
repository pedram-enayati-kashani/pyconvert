from django import template
import jdatetime

register = template.Library()

@register.filter(name='jalali')
def jalali_filter(value, arg='%Y/%m/%d'):
    if not value:
        return ''
    try:
        j_date = jdatetime.datetime.fromgregorian(datetime=value)
        return j_date.strftime(arg)
    except:
        return str(value)