from django import forms
from django.core import validators
from django.utils.html import strip_tags
from module.models.FormBuilder import Form, FormField
from django.core.validators import RegexValidator


class FormBuilderForm(forms.ModelForm):
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

    target_post_type = forms.TypedChoiceField(
        choices=[
            ('post', 'نوشته'),
            ('contact', 'تماس باما'),
            ('general', 'عمومی'),
        ],
        coerce=str,
        initial='post',
        label='برای',
        widget=forms.Select(attrs={'class': 'form-control'})
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
        model = Form
        fields = ['title', 'target_post_type','status']

class FieldBuilderForm(forms.ModelForm):
    # region  field
    label = forms.CharField(
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
        max_length=60,
        error_messages={
            'required': 'نام اجباری می‌باشد',
            'max_length': 'نام نباید بیشتر از 60 کاراکتر باشد',
        },
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9]+(_[A-Za-z0-9]+)*$',
                message='فقط حروف انگلیسی، بدون فاصله، و کلمات با "_" از هم جدا شوند. مثل: first_text',
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="نام پروژه باید از حروف انگلیسی، عدد و فاصله کلمات با _ باشد."
    )

    field_type = forms.TypedChoiceField(
        choices=[
            ("text", "متن کوتاه"),
            ("textarea", "متن بلند"),
            ("number", "عدد"),
            ("email", "ایمیل"),
            ("checkbox", "چک‌باکس"),
            ("select", "لیست کشویی"),
            ("radio", "دکمه رادیویی"),
        ],
        coerce=str,
        initial='text',
        label='نوع',
        widget=forms.Select(attrs={'class': 'form-control'})
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

    required = forms.BooleanField(
        label='اجباری باشد؟',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    prefix = forms.CharField(
        label='پیشوند',
        max_length=50,
        required=False,
        error_messages={
            'max_length': 'پیشوند نباید بیشتر از 50 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    suffix = forms.CharField(
        label='پسوند',
        max_length=50,
        required=False,
        error_messages={
            'max_length': 'پسوند نباید بیشتر از 50 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    options = forms.CharField(
        label='گزینه‌ها (با کاما جدا کنید)',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'گزینه۱, گزینه۲, گزینه۳'}),
        help_text="فقط برای لیست کشویی، رادیویی و چک‌باکس استفاده می‌شود."
    )

    # endregion
    class Meta:
        model = FormField
        fields = ['label','name', 'field_type','status','required','prefix','suffix','options']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = self._meta.model.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("این نام قبلاً ثبت شده است.")

        return name