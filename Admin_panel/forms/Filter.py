from django import forms
from django.utils.translation import gettext_lazy as _

class FilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[
            ('all', _('All')),
            ('draft', _('Draft')),
            ('pending', _('Pending')),
            ('published', _('Published')),
            ('rejected', _('Rejected')),
        ],
        label=_('Status'),
        initial='all',
        required=False,
        widget = forms.Select(attrs={'class': 'form-select'})
    )

    title = forms.CharField(
        label=_('Title'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search in title...')
        }),
    )