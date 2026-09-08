from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from App_panel.models.CommentsModel import Comments
from App_panel.models.PostModel import Post
from App_panel.models.UsersModel import Users


class CommentForm(forms.ModelForm):
    # region Fields

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
            'required': 'فیلد نظر نمی تونه خالی باشه!!',
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    response = forms.CharField(
        label='پاسخ',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    post = forms.ModelChoiceField(
        queryset=Post.objects.filter(status='published'),
        label='نوشته',
        empty_label=None,
        error_messages={
            'required': 'انتخاب نوشته اجباری می‌باشد',
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    parent = forms.ModelChoiceField(
        queryset=Comments.objects.filter(status='approved'),
        label='فرزند نظر',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    status = forms.TypedChoiceField(
        choices=[
            ('approved', 'تایید شده'),
            ('rejected', 'رد شده'),
            ('pending', 'در انتظار تایید'),
        ],
        coerce=str,
        initial='pending',
        label='وضعیت',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    user = forms.ModelChoiceField(
        queryset=Users.objects.filter(is_active=True),
        label='نویسنده',
        required=False,
        error_messages={
            'required': 'انتخاب نویسنده اجباری می‌باشد',
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # endregion
    class Meta:
        model = Comments
        fields = ['fullName','email','body', 'response', 'post', 'parent','status','user']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields['user'].initial = user