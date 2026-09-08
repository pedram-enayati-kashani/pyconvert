# yourapp/templatetags/farsi_lorem.py
from django import template
import random

register = template.Library()

PERSIAN_TEXTS = [
    "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است.",
    "چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است.",
    "در این صورت به نام خود این متن چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی مورد نیاز و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد.",
    "کتابهای زیادی در شصت و سه درصد گذشته حال و آینده شناخت فراوان جامعه و متخصصان را می طلبد.",
    "طراحان رایانه ای علی الخصوص کسانی که با تولید محتوای دیجیتال سر و کار دارند باید با این متن ساختگی کار کنند."
]

@register.simple_tag
def farsi_lorem(count=1, unit='p'):
    """
    تولید متن فارسی فیلر
    واحد: 'p' = پاراگراف، 'w' = کلمه، 's' = جمله
    """
    if unit == 'w':
        words = " ".join(PERSIAN_TEXTS).split()[:count]
        return " ".join(words)
    elif unit == 's':
        sentences = [text.split('،')[0] for text in PERSIAN_TEXTS[:count]]
        return " ".join(sentences)
    else:  # پاراگراف
        return " ".join(random.choices(PERSIAN_TEXTS, k=count))