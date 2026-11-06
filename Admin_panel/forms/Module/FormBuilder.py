from django import forms
from django.core import validators
from django.utils.html import strip_tags
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from module.models.FormBuilder import Form, FormField
from django.core.validators import RegexValidator


class FormBuilderForm(forms.ModelForm):
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

    target_post_type = forms.TypedChoiceField(
        choices=[
            ('post', _('Post')),
            ('contact', _('Contact Us')),
            ('general', _('General')),
        ],
        coerce=str,
        initial='post',
        label=_('For'),
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

    # endregion
    class Meta:
        model = Form
        fields = ['title', 'target_post_type','status']

    def __init__(self, *args, user=None, request=None, **kwargs):
        self.request = request

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        super().__init__(*args, **kwargs)


    def save(self, commit=True):
        """Save with automatic language setting."""
        instance = super().save(commit=False)
        instance.lang = self.lang

        if commit:
            instance.save()
            self.save_m2m()

        return instance

class FieldBuilderForm(forms.ModelForm):
    # region  field
    label = forms.CharField(
        label=_('Label'),
        max_length=120,
        error_messages={
            'required': _("Label is required."),
            'max_length': _("Label cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    name = forms.CharField(
        label=_('Name'),
        max_length=60,
        error_messages={
            'required': _("Name is required."),
            'max_length': _("Name cannot be more than %(limit_value)d characters."),
        },
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9]+(_[A-Za-z0-9]+)*$',
                message=_("Only English letters, no spaces, and separate words with '_'. Example: first_text"),
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=_("Name must contain English letters, numbers, and separate words with _.")
    )

    field_type = forms.TypedChoiceField(
        choices=[
            ("text", _("Short text")),
            ("textarea", _("Long text")),
            ("number", _("Number")),
            ("email", _("Email")),
            ("checkbox", _("Checkbox")),
            ("select", _("Dropdown list")),
            ("radio", _("Radio button")),
        ],
        coerce=str,
        initial='text',
        label=_('Type'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    status = forms.TypedChoiceField(
        choices=[
            ('active', _("Active")),
            ('inactive', _("Inactive")),
        ],
        coerce=str,
        initial='active',
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    required = forms.BooleanField(
        label=_('Is Required?'),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    prefix = forms.CharField(
        label=_('Prefix'),
        max_length=50,
        required=False,
        error_messages={
            'max_length': _("Prefix cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    suffix = forms.CharField(
        label=_('Suffix'),
        max_length=50,
        required=False,
        error_messages={
            'max_length': _("Suffix cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    options = forms.CharField(
        label=_('Options (separated by comma)'),
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': _('Option 1, Option 2, Option 3')
        }),
        help_text=_("Used only for dropdown list, radio, and checkbox.")
    )

    # endregion
    class Meta:
        model = FormField
        fields = ['label', 'name', 'field_type', 'status', 'required', 'prefix', 'suffix', 'options']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = self._meta.model.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(_("This name already exists."))

        return name