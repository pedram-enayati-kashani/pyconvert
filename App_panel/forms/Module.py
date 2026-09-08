from django import forms
from django.core import validators
from django.utils.html import strip_tags
from django_ckeditor_5.widgets import CKEditor5Widget
from App_panel.models.Modules import Modules
from django.core.validators import RegexValidator


class ModuleForm(forms.ModelForm):
    # region  field
    title = forms.CharField(
        label='عنوان',
        max_length=60,
        error_messages={
            'required': 'عنوان اجباری می‌باشد',
            'max_length': 'عنوان نباید بیشتر از 60 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    name = forms.CharField(
        label='نام',
        max_length=60,
        error_messages={
            'required': 'عنوان اجباری می‌باشد',
            'max_length': 'عنوان نباید بیشتر از 60 کاراکتر باشد',
        },
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]+(_[A-Za-z]+)*$',
                message='فقط حروف انگلیسی، بدون فاصله، و کلمات با "_" از هم جدا شوند. مثل: first_text',
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
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
        model = Modules
        fields = ['title', 'name','status']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        query = Modules.objects.filter(name=name)

        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError('این نام قبلاً ثبت شده است، لطفاً نام دیگری انتخاب کنید.')

        return name
