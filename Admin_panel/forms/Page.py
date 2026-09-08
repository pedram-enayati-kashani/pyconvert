from django import forms
from django.core import validators
from django.utils.html import strip_tags
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.validators import RegexValidator
from App_panel.models import Page


class PageForm(forms.ModelForm):
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

    body = forms.CharField(
        label='توضیحات',
        error_messages={
            'required': 'توضیحات اجباری می‌باشد',
        },
        required=False,
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
        label='عکس صفحه',
        required=False,
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
        model = Page
        fields = ['title', 'title_seo', 'body', 'description_seo','image','status','slug']

    # def clean_description(self):
    #     body = self.cleaned_data.get('body', '')
    #     text_only = strip_tags(body).strip()
    #     if not text_only:
    #         raise forms.ValidationError('فیلد توضیحات نمی‌تواند خالی باشد.')
    #     elif text_only == '&nbsp;':
    #         raise forms.ValidationError('فیلد توضیحات نمی‌تواند خالی باشد.')
    #     return body

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            qs = self._meta.model.all_objects.filter(slug__iexact=slug)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("این اسلاگ قبلاً ثبت شده است.")

        return slug