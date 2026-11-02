from django import forms
from django.utils.translation import gettext_lazy as _
from App_panel.models.SiteInfoModel import SiteInfo
from PIL import Image


class SiteInfoForm(forms.ModelForm):
    title = forms.CharField(
        label=_('Title'),
        max_length=200,
        error_messages={
            'required': _("Title is required."),
            'max_length': _("Title cannot be more than %(limit_value)d characters."),
        },
        help_text=_("Maximum 200 characters."),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    title_seo = forms.CharField(
        label=_('Meta title'),
        max_length=60,
        required=False,
        error_messages={
            'max_length': _("Meta title cannot be more than %(limit_value)d characters."),
        },
        help_text=_("Between 30 and 60 characters."),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description_seo = forms.CharField(
        label=_('Meta description'),
        max_length=160,
        required=False,
        error_messages={
            'max_length': _("Meta description cannot be more than %(limit_value)d characters."),
        },
        help_text=_("Between 100 and 160 characters."),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    logo = forms.ImageField(
        label=_('Site Logo'),
        required=False,
        help_text=_("Recommended: 300x100 or SVG."),
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    favicon = forms.ImageField(
        label=_('Site Icon'),
        required=False,
        help_text=_("Image must be square and at least 512x512 pixels (PNG or SVG)."),
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    headMeta = forms.CharField(
        label=_('Head Meta Tags'),
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'dir': 'ltr'
        }),
    )

    footerScript = forms.CharField(
        label=_('Footer Scripts'),
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'dir': 'ltr'
        }),
    )

    robotsText = forms.CharField(
        label=_('robots.txt Content'),
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'dir': 'ltr'
        }),
    )

    class Meta:
        model = SiteInfo
        fields = ['title', 'title_seo', 'description_seo', 'logo', 'favicon', 'headMeta', 'footerScript', 'robotsText']

    def clean_favicon(self):
        favicon = self.cleaned_data.get("favicon")

        if not favicon:
            return favicon

        img = Image.open(favicon)
        width, height = img.size

        # being square
        if width != height:
            raise forms.ValidationError(_("The icon must be square (equal width and height)."))

        # Minimum size
        if width < 512 or height < 512:
            raise forms.ValidationError(_("The image size must be at least 512x512 pixels."))

        return favicon