from django import forms
from django.utils.translation import gettext_lazy as _
from module.models.WaterMarkModel import WaterMark


class WaterMarkForm(forms.ModelForm):

    # region fields

    image = forms.ImageField(
        label=_("Image"),
        required=True,
        error_messages={
            "required": _("image is required.")
        },
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control"
        })
    )

    status = forms.TypedChoiceField(
        label=_("Status"),
        choices=[
            ("active", _("Active")),
            ("inactive", _("Inactive")),
        ],
        coerce=str,
        initial="active",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    width_mode = forms.TypedChoiceField(
        label=_("Width Mode"),
        choices=[
            ("auto", _("Automatic (Percentage)")),
            ("manual", _("Manual (Pixel)")),
            ("self-wh", _("Image's own width")),
        ],
        coerce=str,
        initial="auto",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    height_mode = forms.TypedChoiceField(
        label=_("Height Mode"),
        choices=[
            ("auto", _("Automatic (Percentage)")),
            ("manual", _("Manual (Pixel)")),
            ("self-wh", _("Image's own height")),
        ],
        coerce=str,
        initial="auto",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    width_percent = forms.IntegerField(
        label=_("Width Percentage"),
        required=False,
        min_value=1,
        max_value=100,
        help_text=_("Used if width mode is set to automatic."),
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    height_percent = forms.IntegerField(
        label=_("Height Percentage"),
        required=False,
        min_value=1,
        max_value=100,
        help_text=_("Used if height mode is set to automatic."),
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    manual_width = forms.IntegerField(
        label=_("Width (Pixel)"),
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    manual_height = forms.IntegerField(
        label=_("Height (Pixel)"),
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    position = forms.TypedChoiceField(
        label=_("Position"),
        choices=[
            ('top-left', _('Top Left')),
            ('top-center', _('Top Center')),
            ('top-right', _('Top Right')),
            ('center-left', _('Center Left')),
            ('center', _('Center')),
            ('center-right', _('Center Right')),
            ('bottom-left', _('Bottom Left')),
            ('bottom-center', _('Bottom Center')),
            ('bottom-right', _('Bottom Right')),
        ],
        coerce=str,
        initial="bottom-right",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    opacity = forms.IntegerField(
        label=_("Opacity"),
        min_value=0,
        max_value=100,
        initial=70,
        help_text=_("Number between 0 and 100"),
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    padding = forms.IntegerField(
        label=_("Padding from Image Edge"),
        min_value=0,
        initial=10,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    # endregion

    class Meta:
        model = WaterMark
        fields = [
            "image",
            "status",
            "width_mode",
            "height_mode",
            "width_percent",
            "height_percent",
            "manual_width",
            "manual_height",
            "position",
            "opacity",
            "padding",
        ]

    def __init__(self, *args, request=None, **kwargs):

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

        return instance

    def clean(self):
        cleaned_data = super().clean()

        width_mode = cleaned_data.get("width_mode")
        height_mode = cleaned_data.get("height_mode")

        width_percent = cleaned_data.get("width_percent")
        height_percent = cleaned_data.get("height_percent")
        manual_width = cleaned_data.get("manual_width")
        manual_height = cleaned_data.get("manual_height")

        if width_mode == "auto" and not width_percent:
            self.add_error("width_percent", _("In automatic mode, the width percentage must be specified."))
        if width_mode == "manual" and not manual_width:
            self.add_error("manual_width", _("In manual mode, the width must be specified."))

        if height_mode == "auto" and not height_percent:
            self.add_error("height_percent", _("In automatic mode, the height percentage must be specified."))
        if height_mode == "manual" and not manual_height:
            self.add_error("manual_height", _("In manual mode, the height must be specified."))

        if width_mode == "self-wh" and height_mode == "self-wh":
            self.add_error("width_mode", _("You cannot set both width and height based on the original image dimensions at the same time (the watermark will be distorted)."))

        return cleaned_data