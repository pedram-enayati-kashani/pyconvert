from django import forms
from App_panel.models.SiteInfoModel import SiteInfo
from PIL import Image


class SiteInfoForm(forms.ModelForm):
    title = forms.CharField(
        label='عنوان',
        max_length=120,
        error_messages={
            'required': 'عنوان اجباری می‌باشد',
            'max_length': 'عنوان نباید بیشتر از 120 کاراکتر باشد',
        },
        help_text="حداکثر 120 کاراکتر",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    title_seo = forms.CharField(
        label='عنوان گوگل',
        max_length=60,
        required=False,
        error_messages={
            'max_length': 'عنوان گوگل نباید بیشتر از 60 کاراکتر باشد',
        },
        help_text="بین 30 تا 60 کاراکتر",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description_seo = forms.CharField(
        label='توضیحات گوگل',
        max_length=160,
        required=False,
        error_messages={
            'max_length': 'توضیحات گوگل نباید بیشتر از 160 کاراکتر باشد',
        },
        help_text="بین 100 تا 160 کاراکتر",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    logo = forms.ImageField(
        label='عکس بخش',
        required=False,
        help_text="پیشنهاد: 300×100 یا SVG",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    favicon = forms.ImageField(
        label='عکس بخش',
        required=False,
        help_text="تصویر باید مربع و حداقل 512×512 پیکسل باشد (PNG یا SVG)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    headMeta = forms.CharField(
        label='متا های درون هد',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'dir':'ltr'
        }),
    )

    footerScript = forms.CharField(
        label='اسکریپت های درون فوتر',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'dir':'ltr'
        }),
    )

    robotsText = forms.CharField(
        label='محتوای درون robots.text',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'dir':'ltr'
        }),
    )

    class Meta:
        model = SiteInfo
        fields = ['title', 'title_seo', 'description_seo','logo','favicon','headMeta','footerScript','robotsText']

    def clean_favicon(self):
        favicon = self.cleaned_data.get("favicon")

        if not favicon:
            return favicon

        img = Image.open(favicon)
        width, height = img.size

        # being square
        if width != height:
            raise forms.ValidationError("ایکون باید مربع باشد (عرض و ارتفاع برابر).")

        # Minimum size
        if width < 512 or height < 512:
            raise forms.ValidationError("اندازه تصویر باید حداقل 512×512 باشد.")

        return favicon
