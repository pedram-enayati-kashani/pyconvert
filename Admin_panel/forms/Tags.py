import re
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.validators import RegexValidator
from App_panel.models import Tag


class TagForm(forms.ModelForm):
    # region Fields
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
        label='عکس',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    status = forms.TypedChoiceField(
        choices=[
            ('draft', 'پیش نویس'),
            ('pending', 'در انتظار تایید'),
            ('published', 'منتشر شده'),
            ('rejected', 'رد شده'),
        ],
        coerce=str,
        initial='published',
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
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="این قسمت به صورت خودکار تولید می شود، اما قابل ویرایش است."
    )

    # endregion
    class Meta:
        model = Tag
        fields = ['title', 'title_seo', 'description', 'description_seo','image','status','slug']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # region  check if user is author or not
        if user.groups.filter(name="author").exists():
            self.fields['status'].choices = [
                ('draft', 'پیش نویس'),
                ('pending', 'در انتظار تایید'),
            ]
        # endregion

    # region clean Fields
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
        slug = self.cleaned_data.get('slug')
        if slug:
            qs = self._meta.model.objects.filter(slug__iexact=slug)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("این اسلاگ قبلاً ثبت شده است.")

        return slug
    # endregion