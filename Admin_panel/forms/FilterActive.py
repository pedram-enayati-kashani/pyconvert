from django import forms
from django.utils.translation import gettext_lazy as _

class FilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[
            ('all', _('All')),
            ('active', _('Active')),
            ('inactive', _('Inactive')),
        ],
        label=_('Status'),
        initial='all',
        required=False,
        widget = forms.Select(attrs={'class': 'form-select'})
    )