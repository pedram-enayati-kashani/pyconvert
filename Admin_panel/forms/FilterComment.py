from django import forms
from django.utils.translation import gettext_lazy as _

class FilterCommentForm(forms.Form):
    status = forms.ChoiceField(
        choices=[
            ('all', _('All')),
            ('approved', _('Approved')),
            ('rejected', _('Rejected')),
            ('pending', _('Pending')),
            ('see', _('Seen')),
            ('not-see', _('Unseen')),
        ],
        label=_('Status'),
        initial='all',
        required=False,
        widget = forms.Select(attrs={'class': 'form-select'})
    )