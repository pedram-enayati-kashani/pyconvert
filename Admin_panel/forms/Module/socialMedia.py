from django import forms
from module.models.SocialMediaModel import SocialMedia
from django.core.validators import RegexValidator

class SocialMediaForm(forms.ModelForm):
    # region  field
    title = forms.CharField(
        label='عنوان',
        max_length=120,
        error_messages={
            'required': 'عنوان اجباری می‌باشد',
            'max_length': 'عنوان نباید بیشتر از 120 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    name = forms.CharField(
        label='نام',
        max_length=120,
        error_messages={
            'required': 'نام اجباری می‌باشد',
            'max_length': 'عنوان نباید بیشتر از 120 کاراکتر باشد',
        },
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9]+(_[A-Za-z0-9]+)*$',
                message='فقط حروف انگلیسی، بدون فاصله، و کلمات با "_" از هم جدا شوند. مثل: first_text',
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    url = forms.CharField(
        label='آدرس',
        max_length=120,
        error_messages={
            'required': 'آدرس اجباری می‌باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    rel = forms.MultipleChoiceField(
        choices=[
            ("nofollow", "عدم انتقال اعتبار سئو (nofollow)"),
            ("noopener", "امنیت تب جدید (noopener)"),
            ("noreferrer", "عدم ارسال آدرس مبدا (noreferrer)"),
            ("ugc", "لینک کاربرساز (ugc)"),
            ("sponsored", "لینک تبلیغاتی/اسپانسری (sponsored)"),
        ],
        required=False,
        label="ویژگی rel",
        widget=forms.CheckboxSelectMultiple,
        help_text = "اگر هیچ گزینه‌ای انتخاب نشود، rel خالی می‌ماند (حالت عادی)."
    )

    icon = forms.ImageField(
        label='ایکون',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    target_blank = forms.BooleanField(
        required=False,
        initial=False,
        label="باز شدن در تب جدید"
    )

    status = forms.TypedChoiceField(
        choices=[
            ('active', 'فعال'),
            ('inactive', 'غیرفعال'),
        ],
        coerce=str,
        initial='active',
        label='وضعیت',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # endregion
    class Meta:
        model = SocialMedia
        fields = ['title', 'name','url','status','rel','icon','target_blank']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.rel:
            self.initial["rel"] = self.instance.rel.split()

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = self._meta.model.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("این نام قبلاً ثبت شده است.")

        return name

    def clean_rel(self):
        values = self.cleaned_data.get("rel") or []
        return " ".join(values)