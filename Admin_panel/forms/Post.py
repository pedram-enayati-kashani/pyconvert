import re
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from App_panel.models.PostModel import Post, PostGallery
from App_panel.models.UsersModel import Users
from App_panel.models.SectionModel import Section
from App_panel.models.CategoriesModel import Category
from App_panel.models.TagModel import Tag
from App_panel.models.PageModel import Page
from django.forms import inlineformset_factory
from django.utils.html import strip_tags
from django.core.validators import RegexValidator

class PostForm(forms.ModelForm):
    # region  field
    title = forms.CharField(
        label='عنوان',
        max_length=120,
        error_messages={
            'required': 'عنوان اجباری می‌باشد',
            'max_length': 'عنوان نباید بیشتر از 120 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    title_search = forms.CharField(
        label='عنوان گوگل',
        max_length=60,
        required=False,
        error_messages={
            'max_length': 'عنوان گوگل نباید بیشتر از 60 کاراکتر باشد',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    summery = forms.CharField(
        label='خلاصه',
        max_length=255,
        required=False,
        error_messages={
            'required': 'خلاصه اجباری می‌باشد',
            'max_length': 'خلاصه نباید بیشتر از 255 کاراکتر باشد',
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    summery_search = forms.CharField(
        label='توضیحات گوگل',
        max_length=160,
        required=False,
        error_messages={
            'max_length': 'توضیحات گوگل نباید بیشتر از 160 کاراکتر باشد',
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    body = forms.CharField(
        label='توضیحات',
        error_messages={
            'required': 'توضیحات اجباری می‌باشد',
        },
        widget=CKEditor5Widget(config_name='default'),
    )

    user = forms.ModelChoiceField(
        queryset=Users.objects.filter(is_active=True),
        label='نویسنده',
        empty_label=None,
        error_messages={
            'required': 'انتخاب نویسنده اجباری می‌باشد',
        },
        widget = forms.Select(attrs={'class': 'form-control'})
    )

    section = forms.ModelChoiceField(
        queryset=Section.objects.filter(status='active',type="post"),
        label='بخش',
        empty_label=None,
        error_messages={
            'required': 'انتخاب بخش اجباری می‌باشد',
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(status='published'),
        label='دسته بندی',
        error_messages={
            'required': 'انتخاب دسته بندی اجباری می‌باشد',
        },
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(status='published'),
        label='برچسب',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    pages = forms.ModelChoiceField(
        queryset=Page.objects.filter(status='active'),
        label='صفحه',
        empty_label=None,
        error_messages={
            'required': 'انتخاب صفحه اجباری می‌باشد',
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    image = forms.ImageField(
        label='عکس نوشته',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    watermark = forms.TypedChoiceField(
        choices=[
            ('active', 'داشته باشد'),
            ('inactive', 'نداشته باشد'),
        ],
        coerce=str,
        initial='active',
        label='واترمارک',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    status = forms.TypedChoiceField(
        choices=[
            ('draft', 'پیش نویس'),
            ('pending', 'در انتظار تایید'),
            ('published', 'منتشر شده'),
            ('rejected', 'رد شده'),
        ],
        coerce=str,
        initial='published',
        label='وضعیت',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    slug_validator = RegexValidator(
        regex=r'^[-\w\u0600-\u06FF]+$',
        message='اسلاگ فقط می‌تواند شامل حروف فارسی، انگلیسی، عدد و خط فاصله باشد.'
    )

    slug = forms.CharField(
        label='اسلاگ (URL)',
        max_length=100,
        required=False,
        validators=[slug_validator],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="این قسمت به صورت خودکار تولید می شود، اما قابل ویرایش است."
    )

    # endregion
    class Meta:
        model = Post
        fields = [
            'title', 'title_search', 'summery', 'summery_search','body',
            'user','section','categories','tags','pages','image',
            'watermark','status','slug'
        ]

    def __init__(self, *args,user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # region  check if user is author or not
        if user.groups.filter(name="author").exists():
            self.fields['status'].choices = [
                ('draft', 'پیش نویس'),
                ('pending', 'در انتظار تایید'),
            ]
        # endregion

    # region clean Fields
    def clean_body(self):
        description = self.cleaned_data.get('body', '')
        text_only = strip_tags(description).strip()
        if not text_only:
            raise forms.ValidationError('فیلد توضیحات نمی‌تواند خالی باشد.')
        elif text_only == '&nbsp;':
            raise forms.ValidationError('فیلد توضیحات نمی‌تواند خالی باشد.')

        pattern = r'<h[1-6](\s[^>]*)?>(\s|&nbsp;|<br\s*/?>)*</h[1-6]>'
        max_iterations = 5
        for _ in range(max_iterations):
            new_description = re.sub(
                pattern,
                '<p></p>',
                description,
                flags=re.IGNORECASE
            )
            if new_description == description:
                break
            description = new_description

        return description

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            qs = self._meta.model.all_objects.filter(slug__iexact=slug)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("این اسلاگ قبلاً ثبت شده است.")

        return slug
    # endregion

class PostGalleryForm(forms.ModelForm):
    class Meta:
        model = PostGallery
        fields = ['image', 'alt_text']
        labels = {
            'image': 'تصویر گالری',
            'alt_text': 'متن جایگزین (سئو)'
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'data-max-size': '10485760',
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'توضیح کوتاه برای سئو و دسترسی‌پذیری',
                'maxlength': '150'
            }),
        }
        help_texts = {
            'image': 'فرمت‌های مجاز: JPG, PNG, WebP | حداکثر حجم: ۱۰ مگابایت',
            'alt_text': 'این متن برای سئو و کاربران نابینا استفاده می‌شود.'
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            if self.instance.pk is None:
                raise forms.ValidationError('انتخاب تصویر الزامی است.')
            return self.instance.image

        # چک حجم
        if image.size > 10 * 1024 * 1024:  # 10MB
            raise forms.ValidationError('حجم تصویر نباید بیشتر از ۱۰ مگابایت باشد.')

        # چک اکستنشن (سمت سرور)
        ext = image.name.split('.')[-1].lower()
        allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
        if ext not in allowed_extensions:
            raise forms.ValidationError(f'فرمت فایل مجاز نیست. فرمت‌های مجاز: {", ".join(allowed_extensions)}')

        try:
            import magic
            mime = magic.from_buffer(image.read(1024), mime=True)
            image.seek(0)
            if not mime.startswith('image/'):
                raise forms.ValidationError('فایل ارسالی یک تصویر معتبر نیست.')
        except ImportError:
            pass

        return image

    def clean_alt_text(self):
        alt_text = self.cleaned_data.get('alt_text', '').strip()
        return strip_tags(alt_text)


PostGalleryFormSet = inlineformset_factory(
    Post,
    PostGallery,
    form=PostGalleryForm,  # ← حالا این فرم وجود داره!
    extra=0,
    can_delete=True,
    validate_min=False,
    validate_max=False,
    max_num=20,
    fields=['image', 'alt_text'],  # ← اضافه کردن fields برای امنیت بیشتر
)