from django import forms

class FilterCommentForm(forms.Form):
    status = forms.ChoiceField(
        choices=[
            ('all', 'همه'),
            ('approved', 'تایید شده'),
            ('rejected', 'رد شده'),
            ('pending', 'در انتظار تایید'),
            ('see', 'مشاهده شده'),
            ('not-see', 'مشاهده نشده'),
        ],
        label="وضعیت",
        initial='all',
        required=False,
        widget = forms.Select(attrs={'class': 'form-select'})
    )