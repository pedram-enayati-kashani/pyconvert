from django import forms
from module.models.WaterMarkModel import WaterMark


class WaterMarkForm(forms.ModelForm):

    # region fields

    image = forms.ImageField(
        label="تصویر واترمارک",
        required=True,
        error_messages={
            "required": "تصویر واترمارک الزامی است."
        },
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control"
        })
    )

    status = forms.TypedChoiceField(
        label="وضعیت",
        choices=[
            ("active", "فعال"),
            ("inactive", "غیرفعال"),
        ],
        coerce=str,
        initial="active",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    width_mode = forms.TypedChoiceField(
        label="حالت عرض واترمارک",
        choices=[
            ("auto", "اتوماتیک (درصدی)"),
            ("manual", "دستی (پیکسل)"),
            ("self-wh", "عرض خود عکس"),
        ],
        coerce=str,
        initial="auto",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    height_mode = forms.TypedChoiceField(
        label="حالت ارتفاع واترمارک",
        choices=[
            ("auto", "اتوماتیک (درصدی)"),
            ("manual", "دستی (پیکسل)"),
            ("self-wh", "ارتفاع خود عکس"),
        ],
        coerce=str,
        initial="auto",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    width_percent = forms.IntegerField(
        label="درصد عرض واترمارک",
        required=False,
        min_value=1,
        max_value=100,
        help_text="اگر حالت عرض روی اتوماتیک باشد استفاده می‌شود.",
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    height_percent = forms.IntegerField(
        label="درصد ارتفاع واترمارک",
        required=False,
        min_value=1,
        max_value=100,
        help_text="اگر حالت ارتفاع روی اتوماتیک باشد استفاده می‌شود.",
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    manual_width = forms.IntegerField(
        label="عرض واترمارک (پیکسل)",
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    manual_height = forms.IntegerField(
        label="ارتفاع واترمارک (پیکسل)",
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    position = forms.TypedChoiceField(
        label="موقعیت واترمارک",
        choices=[
            ('top-left', 'بالا چپ'),
            ('top-center', 'بالا وسط'),
            ('top-right', 'بالا راست'),
            ('center-left', 'وسط چپ'),
            ('center', 'وسط'),
            ('center-right', 'وسط راست'),
            ('bottom-left', 'پایین چپ'),
            ('bottom-center', 'پایین وسط'),
            ('bottom-right', 'پایین راست'),
        ],
        coerce=str,
        initial="bottom-right",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    opacity = forms.IntegerField(
        label="شفافیت واترمارک",
        min_value=0,
        max_value=100,
        initial=70,
        help_text="عدد بین 0 تا 100",
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    padding = forms.IntegerField(
        label="فاصله از لبه تصویر",
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

    def clean(self):
        cleaned_data = super().clean()

        width_mode = cleaned_data.get("width_mode")
        height_mode = cleaned_data.get("height_mode")

        width_percent = cleaned_data.get("width_percent")
        height_percent = cleaned_data.get("height_percent")
        manual_width = cleaned_data.get("manual_width")
        manual_height = cleaned_data.get("manual_height")

        if width_mode == "auto" and not width_percent:
            self.add_error("width_percent", "در حالت اتوماتیک باید درصد عرض واترمارک مشخص شود.")
        if width_mode == "manual" and not manual_width:
            self.add_error("manual_width", "در حالت دستی باید عرض واترمارک مشخص شود.")

        if height_mode == "auto" and not height_percent:
            self.add_error("height_percent", "در حالت اتوماتیک باید درصد ارتفاع واترمارک مشخص شود.")
        if height_mode == "manual" and not manual_height:
            self.add_error("manual_height", "در حالت دستی باید ارتفاع واترمارک مشخص شود.")

        if width_mode == "self-wh" and height_mode == "self-wh":
            self.add_error("width_mode","نمی‌توانید همزمان عرض و ارتفاع را بر اساس ابعاد اصلی عکس تنظیم کنید (واترمارک تغییر شکل می‌دهد).")

        return cleaned_data
