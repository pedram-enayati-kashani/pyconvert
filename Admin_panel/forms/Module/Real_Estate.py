from django import forms
from django.core.cache import cache
from django.core.exceptions import ValidationError
from module.models.Real_EstateModel import SellBuy, Rent


class SellBuyForm(forms.ModelForm):

    fullname = forms.CharField(
        label='نام کامل',
        max_length=60,
        error_messages={
            'required': 'نام کامل اجباری می‌باشد',
            'max_length': 'نام کامل نباید بیشتر از 60 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    mobile = forms.CharField(
        label='شماره موبایل',
        max_length=15,
        error_messages={
            'required': 'شماره موبایل اجباری می‌باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="پیشنهاد می شه که اول بقیه فیلدها رو تکمیل کنید و در آخر ارسال کد را کلیک کنید."
    )

    type = forms.TypedChoiceField(
        choices=[("", "انتخاب کنید"),('buyer', 'خریدار'), ('seller', 'فروشنده')],
        label='فرم تقاضا',
        error_messages={
            'required': 'فرم تقاضا اجباری می‌باشد',
        },
        coerce=str,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    type_unit = forms.TypedChoiceField(
        choices=[
            ("", "انتخاب کنید"), ("residential", "مسکونی"), ("administrative", "اداری"),
            ("commercial", "تجاری")
             ],
        coerce=str,
        label='نوع واحد',
        error_messages={
            'required': 'نوع واحد اجباری می‌باشد',
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    discharge_unit = forms.TypedChoiceField(
        choices=[("unloading", "در حال تخلیه"), ("discharge", "تخلیه شده")],
        coerce=str,
        label='وضعیت تخلیه',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text = "در صورت انتخاب گزینه 'در حال تخلیه' در قسمت توضیحات تاریخ نهایی تخلیه واحد را وارد کنید"
    )

    description = forms.CharField(
        label='توضیحات',
        error_messages={'required': 'توضیحات اجباری می‌باشد'},
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
    )

    price = forms.CharField(
        label='قیمت',
        error_messages={'required': 'قیمت اجباری می‌باشد'},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً 18 میلیارد'}),
    )

    room_number = forms.IntegerField(
        label='تعداد اتاق',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2', 'min': '1'}),
    )

    floor = forms.IntegerField(
        label='طبقه',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2'}),
        help_text="مقدار 0 همان طبقه همکف است."
    )

    floor_area = forms.IntegerField(
        label='متراژ',
        error_messages={'required': 'متراژ اجباری می‌باشد'},
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
    )

    direction = forms.TypedChoiceField(
        choices=[
            ("", "انتخاب کنید"), ("north", "شمالی"), ("south", "جنوبی"),
            ("east", "شرقی"), ("west", "غربی"), ("east_west", "شرقی غربی"),
            ("north_east", "شمال شرقی"), ("north_west", "شمال غربی"),
            ("south_east", "جنوب شرقی"), ("south_west", "جنوب غربی"),
            ("north_south", "شمالی جنوبی"), ("two_sided", "دو نبش / دو بر"),
            ("three_sided", "سه نبش / سه بر"),
        ],
        coerce=str,
        label='جهت',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    address = forms.CharField(
        label='آدرس',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    )

    status = forms.TypedChoiceField(
        choices=[('completed', 'پایان یافته'), ('in_progress', 'در حال پیگیری')],
        coerce=str,
        label='وضعیت',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        req_type = cleaned_data.get("type")
        errors = {}

        if req_type == "seller":
            if not cleaned_data.get("room_number"):
                errors["room_number"] = "برای فروشنده، تعداد اتاق الزامی است."
            if cleaned_data.get("floor") is None:
                errors["floor"] = "برای فروشنده، طبقه الزامی است."
            if not cleaned_data.get("direction"):
                errors["direction"] = "برای فروشنده، انتخاب جهت الزامی است."
            if not cleaned_data.get("address"):
                errors["address"] = "برای فروشنده، آدرس الزامی است."
            if not cleaned_data.get("discharge_unit"):
                errors["discharge_unit"] = "برای فروشنده، وضعیت تخلیه الزامی است."

        if errors:
            raise ValidationError(errors)

        return cleaned_data

    class Meta:
        model = SellBuy
        fields = [
            'fullname', 'mobile', 'type', 'description', 'price', 'discharge_unit',
            'room_number', 'floor', 'floor_area', 'direction', 'address', 'status',
            'type_unit'
        ]

class RentForm(forms.ModelForm):
    fullname = forms.CharField(
        label='نام کامل',
        max_length=60,
        error_messages={
            'required': 'نام کامل اجباری می‌باشد',
            'max_length': 'نام کامل نباید بیشتر از 60 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    mobile = forms.CharField(
        label='شماره موبایل',
        max_length=15,
        error_messages={
            'required': 'شماره موبایل اجباری می‌باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="پیشنهاد می شه که اول بقیه فیلدها رو تکمیل کنید و در آخر ارسال کد را کلیک کنید."
    )

    type = forms.TypedChoiceField(
        choices=[("", "انتخاب کنید"),('tenant', 'مستأجر'), ('lessor', 'اجاره دهنده/مالک')],
        coerce=str,
        error_messages={
            'required': 'فرم تقاضا اجباری می‌باشد',
        },
        label='فرم تقاضا',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    type_unit = forms.TypedChoiceField(
        choices=[
            ("", "انتخاب کنید"), ("residential", "مسکونی"), ("administrative", "اداری"),
            ("commercial", "تجاری")
             ],
        coerce=str,
        label='نوع واحد',
        error_messages={
            'required': 'نوع واحد اجباری می‌باشد',
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    discharge_unit = forms.TypedChoiceField(
        choices=[("", "انتخاب کنید"),("unloading", "در حال تخلیه"), ("discharge", "تخلیه شده")],
        coerce=str,
        label='وضعیت تخلیه',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="در صورت انتخاب گزینه 'در حال تخلیه' در قسمت توضیحات تاریخ نهایی تخلیه واحد را وارد کنید"
    )

    description = forms.CharField(
        label='توضیحات',
        error_messages={'required': 'توضیحات اجباری می‌باشد'},
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
    )

    has_change = forms.BooleanField(
        label='تبدیل دارد؟',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    price = forms.CharField(
        label='ودیعه/رهن',
        error_messages={'required': 'قیمت اجباری می‌باشد'},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً 1/500 میلیارد'}),
    )

    max_price = forms.CharField(
        label='حداکثر ودیعه/رهن',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً 3 میلیارد'}),
    )

    price_month = forms.CharField(
        label='اجاره ماهانه',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً 45 میلیون'}),
    )

    room_number = forms.IntegerField(
        label='تعداد اتاق',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2', 'min': '1'}),
    )

    floor = forms.IntegerField(
        label='طبقه',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2'}),
        help_text="مقدار 0 همان طبقه همکف است."
    )

    floor_area = forms.IntegerField(
        label='متراژ',
        error_messages={'required': 'متراژ اجباری می‌باشد'},
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
    )

    direction = forms.TypedChoiceField(
        choices=[
            ("", "انتخاب کنید"), ("north", "شمالی"), ("south", "جنوبی"),
            ("east", "شرقی"), ("west", "غربی"), ("east_west", "شرقی غربی"),
            ("north_east", "شمال شرقی"), ("north_west", "شمال غربی"),
            ("south_east", "جنوب شرقی"), ("south_west", "جنوب غربی"),
            ("north_south", "شمالی جنوبی"), ("two_sided", "دو نبش / دو بر"),
            ("three_sided", "سه نبش / سه بر"),
        ],
        coerce=str,
        label='جهت',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    address = forms.CharField(
        label='آدرس',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    )

    status = forms.TypedChoiceField(
        choices=[('completed', 'پایان یافته'), ('in_progress', 'در حال پیگیری')],
        coerce=str,
        label='فرم تقاضا',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        req_type = cleaned_data.get("type")
        errors = {}

        if req_type == "lessor":
            if not cleaned_data.get("room_number"):
                errors["room_number"] = "برای اجاره دهنده/مالک، تعداد اتاق الزامی است."
            if cleaned_data.get("floor") is None:
                errors["floor"] = "برای اجاره دهنده/مالک، طبقه الزامی است."
            if not cleaned_data.get("direction"):
                errors["direction"] = "برای اجاره دهنده/مالک، انتخاب جهت الزامی است."
            if not cleaned_data.get("address"):
                errors["address"] = "برای اجاره دهنده/مالک، آدرس الزامی است."
            if not cleaned_data.get("discharge_unit"):
                errors["discharge_unit"] = "برای اجاره دهنده/مالک، وضعیت تخلیه الزامی است."

        if errors:
            raise ValidationError(errors)

        return cleaned_data

    class Meta:
        model = Rent
        fields = [
            'fullname', 'mobile', 'type', 'description', 'has_change', 'price', 'discharge_unit', 'status',
            'max_price', 'price_month', 'room_number', 'floor', 'floor_area', 'direction', 'address', 'type_unit'
        ]


class FilterSellBuyForm(forms.Form):
    type = forms.ChoiceField(
        choices=[
            ('all', 'همه'),
            ('seller', 'فروشنده'),
            ('buyer', 'خریدار'),
            ('discharge', 'تخلیه'),
        ],
        label="وضعیت",
        initial='all',
        required=False,
        widget = forms.Select(attrs={'class': 'form-select'})
    )

    address = forms.CharField(
        label='آدرس',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'جستجو در عنوان...'
        }),
    )

class FilterRentForm(forms.Form):
    type = forms.ChoiceField(
        choices=[
            ('all', 'همه'),
            ('lessor', 'اجاره دهنده'),
            ('tenant', 'مستأجر'),
            ('discharge', 'تخلیه'),
            ('has_change', 'تبدیل'),
        ],
        label="وضعیت",
        initial='all',
        required=False,
        widget = forms.Select(attrs={'class': 'form-select'})
    )

    address = forms.CharField(
        label='آدرس',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'جستجو در عنوان...'
        }),
    )