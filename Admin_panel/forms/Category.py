import re
from django import forms
from django.core import validators
from django.utils.html import strip_tags
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.validators import RegexValidator
from App_panel.models import Category
from django.utils.translation import gettext_lazy as _
from django.utils import translation


class CategoryForm(forms.ModelForm):
    # region  field
    title = forms.CharField(
        label=_("Title"),
        max_length=60,
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
            'max_length': _("Meta Title cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description = forms.CharField(
        label=_("Description"),
        required=False,
        widget=CKEditor5Widget(config_name='default'),
    )

    description_seo = forms.CharField(
        label=_("Meta Description"),
        max_length=160,
        required=False,
        error_messages={
            'max_length': _("Meta Description cannot be more than %(limit_value)d characters."),
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    image = forms.ImageField(
        label=_("Image"),
        required=False,
        error_messages={
            'max_length': _("Meta Description cannot be more than %(limit_value)d characters."),
        },
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    parent = forms.ModelChoiceField(
        queryset=Category.objects.filter(status='published'),
        label=_("Parent category"),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    status = forms.TypedChoiceField(
        choices=[
            ('all', _('All')),
            ('draft', _('Draft')),
            ('pending', _('Pending')),
            ('published', _('Published')),
            ('rejected', _('Rejected')),
        ],
        coerce=str,
        initial='published',
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

    # endregion

    class Meta:
        model = Category
        fields = ['title', 'title_seo', 'description', 'description_seo', 'image', 'parent', 'status', 'slug']

    def __init__(self, *args, user=None, request=None, **kwargs):
        self.request = request

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        instance = kwargs.get('instance')

        if instance and instance.lang:
            self.lang = instance.lang

        super().__init__(*args, **kwargs)

        if user and user.groups.filter(name="author").exists():
            self.fields['status'].choices = [
                ('draft', _('Draft')),
                ('pending', _('Pending')),
            ]

        parent_qs = Category.objects.filter(
            status='published',
            lang=self.lang,
        )

        if self.instance and self.instance.pk:
            parent_qs = parent_qs.exclude(pk=self.instance.pk)

        self.fields['parent'].queryset = parent_qs

        self.fields['hidden_lang'] = forms.CharField(
            widget=forms.HiddenInput(),
            initial=self.lang,
            required=False
        )

    # region clean Fields
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')

        if slug:
            lang = self.lang
            qs = self._meta.model.all_objects.filter(slug__iexact=slug, lang=lang)

            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    _("This slug already exists for this language.")
                )

        return slug

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

    def save(self, commit=True):
        """ذخیره با تنظیم خودکار زبان"""
        instance = super().save(commit=False)
        instance.lang = self.lang
        if commit:
            instance.save()
            self.save_m2m()

        return instance
    # endregion