import re
from django import forms
from App_panel.models.SectionModel import Section
from django_ckeditor_5.widgets import CKEditor5Widget

class TableSectionForm(forms.Form):

    titles = forms.CharField(
        label='بخش ها',
        help_text='مثال: خبر اصلی=topnews*main , خبر ساید بار=slider*sidebar',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def save(self):
        data = self.cleaned_data['titles']
        items = [i.strip() for i in re.split('[,،]', data) if i.strip()]

        sections = []

        for item in items:
            title = None
            slug = None
            name = None

            # Extract the name part (if * exists)
            if '*' in item:
                item, name = item.split('*', 1)
                name = name.strip()

            # Extract title and slug (if = exists)
            if '=' in item:
                title, slug = item.split('=', 1)
                title = title.strip()
                slug = slug.strip()
            else:
                title = item.strip()

            # Create Section
            section = Section(
                title=title,
                slug=slug if slug else None,
                name=name if name else None
            )

            section.save()
            sections.append(section)

        return sections

class SectionForm(forms.ModelForm):
    name = forms.CharField(
        label='نام',
        max_length=120,
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
        min_length=30,
        required=False,
        error_messages={
            'max_length': 'عنوان گوگل نباید بیشتر از 60 کاراکتر باشد',
            'min_length': 'عنوان گوگل نباید کمتر از 30 کاراکتر باشد'
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
        min_length=100,
        required=False,
        error_messages={
            'max_length': 'توضیحات گوگل نباید بیشتر از 60 کاراکتر باشد',
            'min_length': 'توضیحات گوگل نباید کمتر از 30 کاراکتر باشد'
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

    slug = forms.CharField(
        label='اسلاگ (URL)',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="این قسمت به صورت خودکار تولید می شود، اما قابل ویرایش است."
    )

    class Meta:
        model = Section
        fields = ['name','title', 'title_seo', 'description', 'description_seo','image','display_number','type','status','slug']

    # def clean_description(self):
    #     description = self.cleaned_data.get('description', '')
    #     text_only = strip_tags(description).strip()
    #     if not text_only:
    #         raise forms.ValidationError('فیلد توضیحات نمی‌تواند خالی باشد.')
    #     elif text_only == '&nbsp;':
    #         raise forms.ValidationError('فیلد توضیحات نمی‌تواند خالی باشد.')
    #     return description