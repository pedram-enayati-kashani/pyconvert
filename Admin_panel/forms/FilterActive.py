from django import forms

class FilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[
            ('all', 'همه'),
            ('active', 'فعال'),
            ('inactive', 'غیرفعال'),
        ],
        label="وضعیت",
        initial='all',
        required=False,
        widget = forms.Select(attrs={'class': 'form-select'})
    )