from django import forms
from module.models.Advertising import AdvText, AdvImage
from App_panel.models.PostModel import Post
from App_panel.models.PageModel import Page
from App_panel.models.CategoriesModel import Category
from App_panel.models.TagModel import Tag
from App_panel.models.SectionModel import Section

class AdvTextForm(forms.ModelForm):
    # region  field
    title = forms.CharField(
        label='عنوان',
        max_length=120,
        error_messages={
            'required': 'عنوان اجباری می‌باشد',
            'max_length': 'عنوان نباید بیشتر از 120 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    section = forms.ModelChoiceField(
        queryset=Section.objects.filter(status='active', type="adv_text"),
        label='بخش',
        empty_label=None,
        error_messages={
            'required': 'انتخاب بخش اجباری می‌باشد',
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    url = forms.CharField(
        label='آدرس',
        error_messages={
            'required': 'آدرس اجباری می‌باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    rel = forms.MultipleChoiceField(
        choices=[
            ("nofollow", "عدم انتقال اعتبار سئو (nofollow)"),
            ("noopener", "امنیت تب جدید (noopener)"),
            ("noreferrer", "عدم ارسال آدرس مبدا (noreferrer)"),
            ("ugc", "لینک کاربرساز (ugc)"),
            ("sponsored", "لینک تبلیغاتی/اسپانسری (sponsored)"),
        ],
        required=False,
        label="ویژگی rel",
        widget=forms.CheckboxSelectMultiple,
        help_text = "اگر هیچ گزینه‌ای انتخاب نشود، rel خالی می‌ماند (حالت عادی)."
    )

    address_list = forms.TypedChoiceField(
        choices=[],
        coerce=str,
        label='لیست صفحات سایت',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text = "با انتخاب گزینه های لیست صفحات ادرس صفحه انتخاب شده در فیلد آدرس ثرار خواهد گرفت"
    )

    target_blank = forms.BooleanField(
        required=False,
        initial=False,
        label="باز شدن در تب جدید"
    )

    status = forms.TypedChoiceField(
        choices=[
            ('active', 'فعال'),
            ('inactive', 'غیرفعال'),
        ],
        coerce=str,
        initial='active',
        label='وضعیت',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # endregion
    class Meta:
        model = AdvText
        fields = ['title','section','url','address_list','target_blank','status','rel']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        dynamic_choices = [
            ('', '---------'),
        ]

        # page
        pages = Page.objects.filter(status="active").order_by('id')
        for page in pages:
            dynamic_choices.append((f'page_{page.id}', f'صفحه - {page.title}'))

        # post
        posts = Post.objects.filter(status="published").order_by('id')
        for post in posts:
            dynamic_choices.append((f'post_{post.id}', f'نوشته - {post.title}'))

        # category
        categories = Category.objects.filter(status="published").order_by('id')
        for category in categories:
            dynamic_choices.append(
                (f'cate_{category.id}', f'دسته بندی - {category.title}'))

        # tag
        tags = Tag.objects.filter(status="published").order_by('id')
        for tag in tags:
            dynamic_choices.append((f'tag_{tag.id}', f'برچسب - {tag.title}'))

        # section
        sections = Section.objects.filter(status="active").order_by('id')
        for section in sections:
            dynamic_choices.append((f'sec_{section.id}', f'بخش - {section.title}'))

        self.fields['address_list'].choices = dynamic_choices

        if self.instance and self.instance.pk and self.instance.rel:
            self.initial["rel"] = self.instance.rel.split()

    def clean_rel(self):
        values = self.cleaned_data.get("rel") or []
        return " ".join(values)

class AdvImageForm(forms.ModelForm):
    # region  field
    title = forms.CharField(
        label='عنوان',
        max_length=120,
        error_messages={
            'required': 'عنوان اجباری می‌باشد',
            'max_length': 'عنوان نباید بیشتر از 120 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    section = forms.ModelChoiceField(
        queryset=Section.objects.filter(status='active', type="adv_image"),
        label='بخش',
        empty_label=None,
        error_messages={
            'required': 'انتخاب بخش اجباری می‌باشد',
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    image = forms.ImageField(
        label='عکس',
        error_messages={
            'required': 'عکس اجباری می‌باشد',
        },
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    url = forms.CharField(
        label='آدرس',
        error_messages={
            'required': 'آدرس اجباری می‌باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    rel = forms.MultipleChoiceField(
        choices=[
            ("nofollow", "عدم انتقال اعتبار سئو (nofollow)"),
            ("noopener", "امنیت تب جدید (noopener)"),
            ("noreferrer", "عدم ارسال آدرس مبدا (noreferrer)"),
            ("ugc", "لینک کاربرساز (ugc)"),
            ("sponsored", "لینک تبلیغاتی/اسپانسری (sponsored)"),
        ],
        required=False,
        label="ویژگی rel",
        widget=forms.CheckboxSelectMultiple,
        help_text = "اگر هیچ گزینه‌ای انتخاب نشود، rel خالی می‌ماند (حالت عادی)."
    )

    address_list = forms.TypedChoiceField(
        choices=[],
        coerce=str,
        label='لیست صفحات سایت',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text = "با انتخاب گزینه های لیست صفحات ادرس صفحه انتخاب شده در فیلد آدرس ثرار خواهد گرفت"
    )

    target_blank = forms.BooleanField(
        required=False,
        initial=False,
        label="باز شدن در تب جدید"
    )

    status = forms.TypedChoiceField(
        choices=[
            ('active', 'فعال'),
            ('inactive', 'غیرفعال'),
        ],
        coerce=str,
        initial='active',
        label='وضعیت',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # endregion
    class Meta:
        model = AdvImage
        fields = ['title','section','url','image','address_list','target_blank','status','rel']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        dynamic_choices = [
            ('', '---------'),
        ]

        # page
        pages = Page.objects.filter(status="active").order_by('id')
        for page in pages:
            dynamic_choices.append((f'page_{page.id}', f'صفحه - {page.title}'))

        # post
        posts = Post.objects.filter(status="published").order_by('id')
        for post in posts:
            dynamic_choices.append((f'post_{post.id}', f'نوشته - {post.title}'))

        # category
        categories = Category.objects.filter(status="published").order_by('id')
        for category in categories:
            dynamic_choices.append(
                (f'cate_{category.id}', f'دسته بندی - {category.title}'))

        # tag
        tags = Tag.objects.filter(status="published").order_by('id')
        for tag in tags:
            dynamic_choices.append((f'tag_{tag.id}', f'برچسب - {tag.title}'))

        # section
        sections = Section.objects.filter(status="active").order_by('id')
        for section in sections:
            dynamic_choices.append((f'sec_{section.id}', f'بخش - {section.title}'))

        self.fields['address_list'].choices = dynamic_choices

        if self.instance and self.instance.pk and self.instance.rel:
            self.initial["rel"] = self.instance.rel.split()

    def clean_rel(self):
        values = self.cleaned_data.get("rel") or []
        return " ".join(values)