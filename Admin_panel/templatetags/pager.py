# your_app/templatetags/pager.py
from django import template

register = template.Library()


@register.simple_tag
def pager(page_obj, paginator):
    # بررسی اولیه برای page_obj و paginator
    if page_obj is None or paginator is None:
        return ""  # بازگرداندن رشته خالی برای نمایش ندادن چیزی

    # اگر تعداد آیتم‌ها صفر بود، صفحه‌بندی نمایش داده نشود
    if paginator.count == 0:
        return ""  # بازگرداندن رشته خالی

    contents = "<div class='pager'>"
    contents += "<ul class='pagination'>"

    # بخش قبلی
    if page_obj.has_previous:
        contents += f"<li><a href='?page={page_obj.previous_page_number()}'>&laquo; قبلی</a></li>"
    else:
        contents += "<li class='disabled'><span>&laquo; قبلی</span></li>"

    for pageNumber in paginator.page_range:
        if page_obj.number == pageNumber:
            contents += f"<li class='active'><span>{pageNumber}</span></li>"
        else:
            contents += f"<li><a href='?page={pageNumber}'>{pageNumber}</a></li>"

    # بخش بعدی
    if page_obj.has_next:
        contents += f"<li><a href='?page={page_obj.next_page_number()}'>بعدی &raquo;</a></li>"
    else:
        contents += "<li class='disabled'><span>بعدی &raquo;</span></li>"

    contents += "</ul>"
    contents += "</div>"
    return contents
