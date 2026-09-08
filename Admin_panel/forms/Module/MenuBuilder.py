from django import forms
from module.models.MenuBuilder import Menu, Menu_Links
from django.core.validators import RegexValidator
from App_panel.models.PostModel import Post
from App_panel.models.PageModel import Page
from App_panel.models.CategoriesModel import Category
from App_panel.models.TagModel import Tag
from App_panel.models.SectionModel import Section
from Admin_panel.helpers.module.menu_builder import build_url_from_target


class MenuBuilderForm(forms.ModelForm):
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

    name = forms.CharField(
        label='نام',
        max_length=60,
        error_messages={
            'required': 'نام اجباری می‌باشد',
            'max_length': 'نام نباید بیشتر از 60 کاراکتر باشد',
        },
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9]+(_[A-Za-z0-9]+)*$',
                message='مقدار به صورت صحیح وارد نشده است!',
            )
        ],
        help_text = 'فقط حروف انگلیسی، بدون فاصله، و کلمات با "_" از هم جدا شوند.  مثل: first_text',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
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
        model = Menu
        fields = ['title', 'name','status']

class LinkForm(forms.ModelForm):
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

    name = forms.CharField(
        label='نام',
        max_length=60,
        error_messages={
            'required': 'عنوان اجباری می‌باشد',
            'max_length': 'عنوان نباید بیشتر از 60 کاراکتر باشد',
        },
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]+(_[A-Za-z]+)*$',
                message='مقدار به صورت صحیح وارد نشده است!',
            )
        ],
        help_text = 'فقط حروف انگلیسی، بدون فاصله، و کلمات با "_" از هم جدا شوند.  مثل: first_text',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    url = forms.CharField(
        label='آدرس',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='اگه این یک ادرس خارج از سایت است ادرس دهید غیر از آن هدف رو انتخاب کنید.',
    )

    parent = forms.ModelChoiceField(
        queryset=Menu_Links.objects.filter(status='active'),
        label='والد لینک',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    address_list = forms.TypedChoiceField(
        choices=[],
        coerce=str,
        label='لیست صفحات سایت',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text = "با انتخاب گزینه های لیست صفحات ادرس صفحه انتخاب شده در فیلد آدرس ثرار خواهد گرفت"
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
        help_text="اگر هیچ گزینه‌ای انتخاب نشود، rel خالی می‌ماند (حالت عادی)."
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
        model = Menu_Links
        fields = ['title','name', 'url','parent','address_list','rel','target_blank','status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # parent
        parent_qs = Menu_Links.objects.filter(status='active')

        if self.instance and self.instance.pk:
            parent_qs = parent_qs.exclude(pk=self.instance.pk)

        self.fields['parent'].queryset = parent_qs

        # region  target
        dynamic_choices = [
            ('', '---------'),
        ]

        # page
        pages = Page.objects.filter(status="active").order_by('id')
        for page in pages:
            dynamic_choices.append((f'page_{page.id}', f'صفحه - {page.title}'))

        # category
        categories = Category.objects.filter(status="published").order_by('id')
        for category in categories:
            dynamic_choices.append(
                (f'cate_{category.id}', f'دسته بندی - {category.title}'))

        # section
        sections = Section.objects.filter(status="active",type__in=['post', 'no_post']).order_by('id')
        for section in sections:
            dynamic_choices.append((f'sec_{section.id}', f'بخش - {section.title}'))

        # sitemap and robots
        dynamic_choices.append(("robots", "Robots.txt"))
        dynamic_choices.append(("sitemap", "Sitemap.xml"))

        self.fields['address_list'].choices = dynamic_choices
        # endregion

        # rel
        if self.instance and self.instance.pk and self.instance.rel:
            self.initial["rel"] = self.instance.rel.split()



    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        address_list = cleaned_data.get("address_list")

        if address_list:
            generated_url = build_url_from_target(address_list)
            if not generated_url:
                raise forms.ValidationError("برای صفحه انتخاب‌شده، آدرس معتبری ساخته نشد.")
            cleaned_data["url"] = generated_url
            return cleaned_data

        if not url:
            raise forms.ValidationError("یا آدرس را وارد کنید یا یکی از لیست صفحات سایت را انتخاب کنید.")

        return cleaned_data


    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = self._meta.model.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("این نام قبلاً ثبت شده است.")

        return name

    def clean_rel(self):
        values = self.cleaned_data.get("rel") or []
        return " ".join(values)