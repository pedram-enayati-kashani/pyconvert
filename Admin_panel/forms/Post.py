import re
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from django.utils.translation import gettext_lazy as _
from django.utils import translation
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
        label= _("Title"),
        max_length=120,
        error_messages={
            'required': _("Title is required."),
            'max_length': _("Title cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    title_search = forms.CharField(
        label=_("Meta title"),
        max_length=60,
        required=False,
        error_messages={
            'max_length': _("Meta Title cannot be more than %(limit_value)d characters.")
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    summary = forms.CharField(
        label=_("Summary"),
        max_length=200,
        required=False,
        error_messages={
            'required': _("Summary is required."),
            'max_length': _("Summary cannot be more than %(limit_value)d characters."),
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    summery_search = forms.CharField(
        label=_("Meta description"),
        max_length=160,
        required=False,
        error_messages={
            'max_length': _("Meta description cannot be more than %(limit_value)d characters."),
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
    )

    body = forms.CharField(
        label=_("Description"),
        error_messages={
            'required': _("Description is required."),
        },
        widget=CKEditor5Widget(config_name='default'),
    )

    user = forms.ModelChoiceField(
        queryset=Users.objects.filter(is_active=True),
        label=_("Author"),
        empty_label=_("Select a author..."),
        error_messages={
            'required': _("Author selection is required."),
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    section = forms.ModelChoiceField(
        queryset=Section.objects.filter(status='active',type="post"),
        label=_("Section"),
        empty_label=_("Select a section..."),
        error_messages={
            'required': _("Section selection is required."),
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(status='published'),
        label=_("Categories"),  # جمع
        error_messages={
            'required': _("Category selection is required."),
        },
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(status='published'),
        label=_("Tags"),  # جمع
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    pages = forms.ModelChoiceField(
        queryset=Page.objects.filter(status='active'),
        label=_("Page"),
        empty_label=_("Select a page..."),
        error_messages={
            'required': _("Page selection is required."),
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    image = forms.ImageField(
        label=_("Image"),
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    watermark = forms.ChoiceField(  # یا TypedChoiceField
        choices=[
            ('active', _('Yes')),
            ('inactive', _('No')),
        ],
        initial='active',
        label=_("Watermark"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    status = forms.TypedChoiceField(
        choices=[
            ('all', _('All')),
            ('draft', _('Draft')),
            ('pending', _('Pending')),
            ('published', _('Published')),
            ('rejected', _('Rejected')),
        ],
        coerce=str,
        initial='published',
        label=_("Status"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    slug_validator = RegexValidator(
        regex=r'^[-\w\u0600-\u06FF]+$',
        message=_(
            "Slug can only contain English and Persian letters, numbers, and hyphens."
        ),
        code='invalid_slug'
    )

    slug = forms.CharField(
        label=_("Slug (URL)"),
        max_length=100,
        required=False,
        validators=[slug_validator],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=_(
            "Auto-generated from title. If left empty, uses title value. Duplicates are handled by appending numbers for uniqueness.")
    )

    # endregion
    class Meta:
        model = Post
        fields = [
            'title', 'title_search', 'summery', 'summery_search','body',
            'user','section','categories','tags','pages','image',
            'watermark','status','slug'
        ]

    def __init__(self, *args,user=None, request=None, **kwargs):

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        instance = kwargs.get('instance')

        if instance and instance.pk and instance.lang:
            self.lang = instance.lang

        super().__init__(*args, **kwargs)
        # region  check if user is author or not
        if user and user.groups.filter(name="author").exists():
            self.fields['status'].choices = [
                ('draft', _('Draft')),
                ('pending', _('Pending')),
            ]
        # endregion

    # region clean Fields
    from django.utils.translation import gettext_lazy as _
    from django.utils.html import strip_tags
    import re

    def clean_body(self):
        body = self.cleaned_data.get('body', '')

        if not body:
            return body

        pattern = r'<h[1-6](\s[^>]*)?>(\s|&nbsp;|<br\s*/?>)*</h[1-6]>'
        max_iterations = 5
        for _ in range(max_iterations):
            new_body = re.sub(
                pattern,
                '<p></p>',
                body,
                flags=re.IGNORECASE
            )
            if new_body == body:
                break
            body = new_body

        text_only = strip_tags(body).replace('&nbsp;', '').strip()

        if not text_only:
            raise forms.ValidationError(
                _("Body field cannot be empty.")
            )

        return body

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')

        if slug:
            lang = self.lang
            qs = self._meta.model.objects.filter(slug__iexact=slug, lang=lang)

            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    _("This slug already exists for this language.")
                )

        return slug
    # endregion

class PostGalleryForm(forms.ModelForm):
    class Meta:
        model = PostGallery
        fields = ['image', 'alt_text']
        labels = {
            'image': _('Gallery image'),
            'alt_text': _('Alt text (SEO)')
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'data-max-size': '10485760',
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Short description for SEO and accessibility'),
                'maxlength': '150'
            }),
        }
        help_texts = {
            'image': _('Allowed formats: JPG, PNG, WebP | Max size: 10 MB'),
            'alt_text': _('This text is used for SEO and visually impaired users.')
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            if self.instance.pk is None:
                raise forms.ValidationError(_('Image selection is required.'))
            return self.instance.image

        if image.size > 10 * 1024 * 1024:  # 10MB
            raise forms.ValidationError(_('Image size cannot exceed 10 MB.'))

        ext = image.name.split('.')[-1].lower()
        allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
        if ext not in allowed_extensions:
            raise forms.ValidationError(
                _('File format not allowed. Allowed formats: %(exts)s') % {
                    'exts': ', '.join(allowed_extensions)
                }
            )
        try:
            import magic
            mime = magic.from_buffer(image.read(1024), mime=True)
            image.seek(0)
            if not mime.startswith('image/'):
                raise forms.ValidationError(_('The uploaded file is not a valid image.'))
        except ImportError:
            pass

        return image

    def clean_alt_text(self):
        alt_text = self.cleaned_data.get('alt_text', '').strip()
        return strip_tags(alt_text)


PostGalleryFormSet = inlineformset_factory(
    Post,
    PostGallery,
    form=PostGalleryForm,
    extra=0,
    can_delete=True,
    validate_min=False,
    validate_max=False,
    max_num=20,
    fields=['image', 'alt_text'],
)