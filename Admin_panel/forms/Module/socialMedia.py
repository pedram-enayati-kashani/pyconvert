from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from module.models.SocialMediaModel import SocialMedia

class SocialMediaForm(forms.ModelForm):
    # region  field
    title = forms.CharField(
        label=_('Title'),
        max_length=120,
        error_messages={
            'required': _("Title is required."),
            'max_length': _("Title cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    name = forms.CharField(
        label=_('Name'),
        max_length=120,
        error_messages={
            'required': _("Name is required."),
            'max_length': _("Name cannot be more than %(limit_value)d characters."),
        },
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9]+(_[A-Za-z0-9]+)*$',
                message=_('Only English letters, no spaces, and separate words with "_". Example: first_text'),
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    url = forms.CharField(
        label=_('URL'),
        max_length=120,
        error_messages={
            'required': _("URL is required."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    rel = forms.MultipleChoiceField(
        choices=[
            ("nofollow", _("Do not pass SEO credit (nofollow)")),
            ("noopener", _("New tab security (noopener)")),
            ("noreferrer", _("Do not send referrer (noreferrer)")),
            ("ugc", _("User-generated content link (ugc)")),
            ("sponsored", _("Sponsored/Advertisement link (sponsored)")),
        ],
        required=False,
        label=_("Rel Attribute"),
        widget=forms.CheckboxSelectMultiple,
        help_text=_("If no option is selected, rel will remain empty (normal mode).")
    )

    icon = forms.ImageField(
        label=_('Icon'),
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    target_blank = forms.BooleanField(
        required=False,
        initial=False,
        label=_("Open in new tab")
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

    # endregion
    class Meta:
        model = SocialMedia
        fields = ['title', 'name', 'url', 'status', 'rel', 'icon', 'target_blank']

    def __init__(self, *args, request=None, **kwargs):

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.rel:
            self.initial["rel"] = self.instance.rel.split()

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = self._meta.model.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(_("This name already exists."))

        return name

    def clean_rel(self):
        values = self.cleaned_data.get("rel") or []
        return " ".join(values)

    def save(self, commit=True):
        """Save with automatic language setting."""
        instance = super().save(commit=False)
        instance.lang = self.lang

        if commit:
            instance.save()

        return instance