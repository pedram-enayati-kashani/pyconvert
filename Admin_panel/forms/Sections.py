import re
from django import forms
from django.core import validators
from django.utils.html import strip_tags
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.validators import RegexValidator
from App_panel.models import Section

class SectionForm(forms.ModelForm):
    name = forms.CharField(
        label='نام',
        max_length=120,
        required=False,
        error_messages={
            'required': 'نام اجباری می‌باشد',
            'max_length': 'نام نباید بیشتر از 120 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    title = forms.CharField(
        label='عنوان',
        max_length=120,
        error_messages={
            'required': 'عنوان اجباری می‌باشد',
            'max_length': 'عنوان نباید بیشتر از 120 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    title_seo = forms.CharField(
        label='عنوان گوگل',
        max_length=60,
        required=False,
        error_messages={
            'max_length': 'عنوان گوگل نباید بیشتر از 60 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description = forms.CharField(
        label='توضیحات',
        required=False,
        error_messages={
            'required': 'توضیحات اجباری می‌باشد',
        },
        widget=CKEditor5Widget(config_name='default'),
    )

    description_seo = forms.CharField(
        label='توضیحات گوگل',
        max_length=160,
        required=False,
        error_messages={
            'max_length': 'توضیحات گوگل نباید بیشتر از 60 کاراکتر باشد',
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    image = forms.ImageField(
        label='عکس بخش',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    display_number = forms.IntegerField(
        label='تعداد نمایش',
        min_value=1,
        initial=1,
        required=True,
        error_messages={
            'min_value': 'کمترین مقدار 1 می باشد',
            'required': 'تعداد نمایش اجباری می‌باشد',
        },
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    type = forms.TypedChoiceField(
        choices=[
            ('post', 'نوشته'),
            ('no_post', 'اطلاعیه بدون نوشته'),
            ('last_news', 'آخرین اخبار'),
            ('most_visited', 'پربازدید ترین'),
            ('most_commented', 'پربحث ترین'),
            ('adv_text', 'تبلیغ متنی'),
            ('adv_image', 'تبلیغ بنر'),
        ],
        coerce=str,
        initial='post',
        label='نوع',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    status = forms.TypedChoiceField(
        choices=[
            ('active', 'فعال'),
            ('inactive', 'غیرفعال')
        ],
        coerce=str,
        initial='active',
        label='وضعیت',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    slug_validator = RegexValidator(
        regex=r'^[-\w\u0600-\u06FF]+$',
        message='اسلاگ فقط می‌تواند شامل حروف فارسی، انگلیسی، عدد و خط فاصله باشد.'
    )

    slug = forms.CharField(
        label='اسلاگ (URL)',
        max_length=100,
        required=False,
        validators=[slug_validator],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="این قسمت به صورت خودکار تولید می شود، اما قابل ویرایش است."
    )

    class Meta:
        model = Section
        fields = ['name','title', 'title_seo', 'description', 'description_seo','image','display_number','type','status','slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # in update
        if self.instance and self.instance.pk:
            self.fields['name'].disabled = True
            self.fields['type'].disabled = True
            self.fields['slug'].disabled = True

    def clean_description(self):
        description = self.cleaned_data.get('description', '')

        if not description:
            return description
        pattern = r'<h[1-6](\s[^>]*)?>(\s|&nbsp;|<br\s*/?>)*</h[1-6]>'
        max_iterations = 5
        for _ in range(max_iterations):
            new_description = re.sub(
                pattern,
                '<p></p>',
                description,
                flags=re.IGNORECASE
            )
            if new_description == description:
                break
            description = new_description

        return description

    def clean_slug(self):
        if self.instance and self.instance.pk:
            return self.instance.slug
        slug = self.cleaned_data.get('slug')
        if slug:
            qs = self._meta.model.all_objects.filter(slug__iexact=slug)
            if qs.exists():
                raise forms.ValidationError("این اسلاگ قبلاً ثبت شده است.")
        return slug

    def clean_name(self):
        if self.instance and self.instance.pk:
            return self.instance.name
        name = self.cleaned_data.get('name')
        qs = self._meta.model.objects.filter(name__iexact=name)
        if qs.exists():
            raise forms.ValidationError("این نام قبلاً ثبت شده است.")
        return name

    def clean_type(self):
        if self.instance and self.instance.pk:
            return self.instance.type
        return self.cleaned_data.get('type')