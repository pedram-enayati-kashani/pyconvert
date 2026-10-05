import re
from django import forms
from django.utils import translation
from django_ckeditor_5.widgets import CKEditor5Widget
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from App_panel.models import Section

class SectionForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name"),
        max_length=120,
        required=False,
        error_messages={
            'required': _("Name is required."),
            'max_length': _("Name cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    title = forms.CharField(
        label=_("Title"),
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

    description = forms.CharField(
        label=_("Description"),
        required=False,
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

    display_number = forms.IntegerField(
        label=_('Display count'),
        min_value=1,
        initial=1,
        error_messages={
            'min_value': _('Minimum value is 1.'),
            'required': _('Display count is required.'),
        },
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    type = forms.TypedChoiceField(
        choices=[
            ('post', _('All')),
            ('no_post', _('Without post')),
            ('last_news', _('Last posts')),
            ('most_visited', _('Most visited')),
            ('most_commented', _('Most commented')),
            ('adv_text', _('Text advertisement')),
            ('adv_image', _('Banner advertisement')),
        ],
        coerce=str,
        initial='post',
        label=_("Type"),
        widget=forms.Select(attrs={'class': 'form-control'})
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
        model = Section
        fields = ['name','title', 'title_seo', 'description', 'description_seo','image','display_number','type','status','slug']

    def __init__(self, *args, request=None, **kwargs):

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        instance = kwargs.get('instance')

        if instance and instance.pk and instance.lang:
            self.lang = instance.lang

        super().__init__(*args, **kwargs)

        # in update
        if self.instance and self.instance.pk:
            self.fields['name'].disabled = True
            self.fields['type'].disabled = True
            self.fields['slug'].disabled = True

        self.fields['hidden_lang'] = forms.CharField(
            widget=forms.HiddenInput(),
            initial=self.lang,
            required=False
        )

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
            lang = self.lang
            qs = self._meta.model.all_objects.filter(slug__iexact=slug, lang=lang)

            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    _("This slug already exists for this language.")
                )

        return slug

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            return name

        lang = self.lang
        qs = self._meta.model.all_objects.filter(name__iexact=name, lang=lang)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                _("This name already exists.")
            )

        return name

    def clean_type(self):
        if self.instance and self.instance.pk:
            return self.instance.type
        return self.cleaned_data.get('type')

    def save(self, commit=True):
        """Save with automatic language setting."""
        instance = super().save(commit=False)
        instance.lang = self.lang

        if commit:
            instance.save()
            self.save_m2m()

        return instance