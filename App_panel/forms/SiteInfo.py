import re
from django import forms
from PIL import Image
from ..models.SiteInfoModel import SiteInfo
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site

class SiteInfoForm(forms.ModelForm):

    title = forms.CharField(
        label='عنوان',
        max_length=120,
        help_text="حداکثر 120 کاراکتر",
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
        help_text="بین 30 تا 60 کاراکتر",
        error_messages={
            'max_length': 'عنوان گوگل نباید بیشتر از 60 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description_seo = forms.CharField(
        label='توضیحات گوگل',
        max_length=160,
        required=False,
        help_text="بین 100 تا 160 کاراکتر",
        error_messages={
            'max_length': 'توضیحات گوگل نباید بیشتر از 160 کاراکتر باشد',
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    logo = forms.ImageField(
        label='لوگو',
        required=False,
        help_text="پیشنهاد: 300×100 یا SVG",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    favicon = forms.ImageField(
        label='ایکون سایت',
        required=False,
        help_text="تصویر باید مربع و حداقل 512×512 پیکسل باشد (PNG یا SVG)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
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

    domain = forms.CharField(
        label='دامنه سایت',
        max_length=255,
        error_messages={
            'required': 'وارد کردن دامنه اجباری است',
            'max_length': 'دامنه نباید بیشتر از ۲۵۵ کاراکتر باشد',
        },
        help_text="مثال: site.com (بدون http یا https)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example.com'}),
    )

    name = forms.CharField(
        label='نام سایت (نمایشی)',
        max_length=50,
        error_messages={
            'required': 'نام دامنه اجباری می‌باشد',
            'max_length': 'نام دامنه نباید بیشتر از ۵۰ کاراکتر باشد',
        },
        help_text="نامی که در پنل یا سایدبار نمایش داده می‌شود",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'site'}),
    )

    class Meta:
        model = SiteInfo
        fields = ['title', 'title_seo', 'description_seo', 'logo', 'favicon', 'status', 'domain', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        site = Site.objects.filter(id=1).first()
        if site:
            self.fields['domain'].initial = site.domain
            self.fields['name'].initial = site.name

    def save(self, commit=True):
        instance = super().save(commit=False)

        domain = self.cleaned_data.get("domain")
        name = self.cleaned_data.get("name")
        scheme = getattr(self, "domain_scheme", "https")

        if not instance.pk and not instance.robotsText:
            instance.robotsText = f"User-agent: *\nSitemap: https://{domain}/sitemap.xml"

        if commit:
            instance.save()

            site, created = Site.objects.get_or_create(
                id=1,
                defaults={
                    'domain': domain,
                    'name': name,
                }
            )

            if not created:
                site.domain = domain
                site.name = name

            site.save()

        return instance

    def clean_favicon(self):
        favicon = self.cleaned_data.get("favicon")

        if not favicon:
            return favicon

        img = Image.open(favicon)
        width, height = img.size

        if width != height:
            raise forms.ValidationError("ایکون باید مربع باشد (عرض و ارتفاع برابر).")

        if width < 512 or height < 512:
            raise forms.ValidationError("اندازه تصویر باید حداقل 512×512 باشد.")

        return favicon

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
            raise ValidationError("نام سایت فقط باید شامل حروف انگلیسی و اعداد باشد.")
        return name

    def clean_domain(self):
        domain = self.cleaned_data.get('domain', '').strip()
        self.domain_scheme = "https"
        if domain.startswith("http://"):
            self.domain_scheme = "http"
            domain = domain.replace("http://", "", 1)
        elif domain.startswith("https://"):
            self.domain_scheme = "https"
            domain = domain.replace("https://", "", 1)

        domain = domain.strip("/")
        if not re.match(r'^[a-zA-Z0-9\-\.\:]+$', domain):
            raise ValidationError("دامنه فقط باید شامل حروف انگلیسی، اعداد، نقطه، خط تیره و پورت باشد.")

        return domain

