from django import forms
from App_panel.models.CommentsModel import Comments
from captcha.fields import CaptchaField, CaptchaTextInput
from django.core.exceptions import ValidationError

class CommentForm(forms.ModelForm):
    # region  field

    captcha = CaptchaField(
        label="کد امنیتی",
        widget=CaptchaTextInput(attrs={'class': 'form-control', 'placeholder': 'کد را وارد کنید'})
    )

    fullName = forms.CharField(
        label='نام کامل',
        max_length=60,
        error_messages={
            'max_length': 'نام کامل نباید بیشتر از 60 کاراکتر باشد',
            'required': 'نام کامل اجباری می‌باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        label='ایمیل',
        max_length=100,
        error_messages={
            'invalid': 'لطفاً یک ایمیل معتبر وارد کنید',
            'max_length': 'ایمیل نباید بیشتر از 100 کاراکتر باشد',
            'required': 'ایمیل اجباری می‌باشد',
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: info@site.com'
        }),
    )

    body = forms.CharField(
        label='نظر',
        error_messages={
            'required': 'نظر اجباری می‌باشد',
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 12,
        }),
    )

    # endregion
    class Meta:
        model = Comments
        fields = ['fullName', 'email', 'body']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.post_obj = kwargs.pop('post_obj', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.post = self.post_obj

        if commit:
            comment.save()
        return comment


class SubCommentForm(forms.ModelForm):
    # region  field

    fullName = forms.CharField(
        label='نام کامل',
        max_length=120,
        error_messages={
            'required': 'نام کامل اجباری می‌باشد',
            'max_length': 'نام کامل نباید بیشتر از 120 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        label='ایمیل',
        max_length=100,
        error_messages={
            'invalid': 'لطفاً یک ایمیل معتبر وارد کنید',
            'max_length': 'ایمیل نباید بیشتر از 100 کاراکتر باشد',
            'required': 'ایمیل اجباری می‌باشد',
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: info@site.com'
        }),
    )

    body = forms.CharField(
        label='نظر',
        error_messages={
            'required': 'نظر اجباری می‌باشد',
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
        }),
    )

    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    phone = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    # endregion
    class Meta:
        model = Comments
        fields = ['fullName', 'email', 'body', 'parent_id',"phone"]

    def __init__(self, *args, **kwargs):
        self.post_obj = kwargs.pop('post_obj', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.post = self.post_obj

        parent_id = self.cleaned_data.get('parent_id')
        if parent_id:
            comment.parent_id = parent_id

        if commit:
            comment.save()
        return comment

    def clean_phone(self):
        """If the website's hidden field is filled in, the comment is spam."""
        value = self.cleaned_data.get('phone')
        if value:
            raise ValidationError("Spam detected!")
        return value