import re
from django import forms
from django.core import validators
from django.utils.html import strip_tags
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.validators import RegexValidator
from App_panel.models import Page
from django.utils.translation import gettext_lazy as _

class PageForm(forms.ModelForm):
    title = forms.CharField(
        label= _("Title"),
        max_length=120,
        error_messages={
            'required': _("Title is required."),
            'max_length': _("Title cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    title_seo = forms.CharField(
        label=_("Meta title"),
        max_length=60,
        required=False,
        error_messages={
            'max_length': _("Meta Title cannot be more than %(limit_value)d characters.")
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    body = forms.CharField(
        label=_("Description"),
        widget=CKEditor5Widget(config_name='default'),
    )

    description_seo = forms.CharField(
        label=_("Meta description"),
        max_length=160,
        required=False,
        error_messages={
            'max_length': _("Meta description cannot be more than %(limit_value)d characters."),
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    image = forms.ImageField(
        label=_("Image"),
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    status = forms.TypedChoiceField(
        choices=[
            ('active', _("Active")),
            ('inactive', _("Inactive"))
        ],
        coerce=str,
        initial='active',
        label=_("Status"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    slug_validator = RegexValidator(
        regex=r'^[-\w\u0600-\u06FF]+$',
        message=_(
            "Slug can only contain English and Persian letters, numbers, and hyphens."
        ),
        code='invalid_slug'
    )

    slug = forms.CharField(
        label=_("Slug (URL)"),
        max_length=100,
        required=False,
        validators=[slug_validator],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=_(
            "Auto-generated from title. If left empty, uses title value. Duplicates are handled by appending numbers for uniqueness.")
    )

    class Meta:
        model = Page
        fields = ['title', 'title_seo', 'body', 'description_seo','image','status','slug']

    def __init__(self, *args, user=None, request=None, **kwargs):
        self.request = request

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        super().__init__(*args, **kwargs)

    def clean_body(self):
        body = self.cleaned_data.get('body', '')

        if not body:
            return body
        pattern = r'<h[1-6](\s[^>]*)?>(\s|&nbsp;|<br\s*/?>)*</h[1-6]>'
        max_iterations = 5
        for _ in range(max_iterations):
            new_body = re.sub(
                pattern,
                '<p>&nbsp;</p>',
                body,
                flags=re.IGNORECASE
            )
            if new_body == body:
                break
            body = new_body

        return body

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')

        if slug:
            lang = self.lang
            qs = self._meta.model.objects.filter(slug__iexact=slug, lang=lang)

            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    _("This slug already exists for this language.")
                )

        return slug

    def save(self, commit=True):
        """Save with automatic language setting."""
        instance = super().save(commit=False)
        instance.lang = self.lang

        if commit:
            instance.save()
            self.save_m2m()

        return instance