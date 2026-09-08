from django import forms
from module.models.RedirectRuleModel import RedirectRule

class RedirectRuleForm(forms.ModelForm):
    class Meta:
        model = RedirectRule
        fields = ['old_url', 'new_url', 'is_permanent', 'status']
        labels = {
            'old_url': 'آدرس قدیمی',
            'new_url': 'آدرس جدید',
            'is_permanent': 'دائمی باشد؟',
            'status': 'وضعیت',
        }
        help_texts = {
            'old_url': 'آدرس را بدون دامنه وارد کنید. مثال: /old-page/',
            'new_url': 'آدرس را بدون دامنه وارد کنید. مثال: /new-page/',
        }
        widgets = {
            'old_url': forms.TextInput(attrs={'class': 'form-control'}),
            'new_url': forms.TextInput(attrs={'class': 'form-control'}),
            'is_permanent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['is_permanent'].initial = False
            self.fields['status'].initial = 'active'
