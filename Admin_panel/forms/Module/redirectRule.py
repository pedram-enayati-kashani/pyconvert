from django import forms
from django.utils.translation import gettext_lazy as _, get_language  # ✅ get_language اضافه شد
from module.models.RedirectRuleModel import RedirectRule

class RedirectRuleForm(forms.ModelForm):
    status = forms.TypedChoiceField(
        choices=[
            ('active', _("Active")),
            ('inactive', _("Inactive"))
        ],
        coerce=str,
        initial='active',
        label=_("Status"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = RedirectRule
        fields = ['old_url', 'new_url', 'is_permanent', 'status']
        labels = {
            'old_url': _('Old URL'),
            'new_url': _('New URL'),
            'is_permanent': _('Permanent?'),
        }
        help_texts = {
            'old_url': _('Enter the URL without the domain. Example: /old-page/'),
            'new_url': _('Enter the URL without the domain. Example: /new-page/'),
        }
        widgets = {
            'old_url': forms.TextInput(attrs={'class': 'form-control'}),
            'new_url': forms.TextInput(attrs={'class': 'form-control'}),
            'is_permanent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, request=None, **kwargs):
        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = get_language() or 'fa'
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['is_permanent'].initial = False

    def save(self, commit=True):
        """Save with automatic language setting."""
        instance = super().save(commit=False)
        instance.lang = self.lang

        if commit:
            instance.save()

        return instance