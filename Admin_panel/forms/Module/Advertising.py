from django import forms
from django.utils.translation import gettext_lazy as _
from module.models.Advertising import AdvText, AdvImage
from App_panel.models.PostModel import Post
from App_panel.models.PageModel import Page
from App_panel.models.CategoriesModel import Category
from App_panel.models.TagModel import Tag
from App_panel.models.SectionModel import Section

class AdvTextForm(forms.ModelForm):
    # region  field
    title = forms.CharField(
        label=_("Title"),
        max_length=60,
        error_messages={
            'required': _("Title is required."),
            'max_length': _("Title cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
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

    url = forms.CharField(
        label=_('URL'),
        error_messages={
            'required': _("URL is required."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    rel = forms.MultipleChoiceField(
        choices=[
            ("nofollow", _("Do not pass SEO credit (nofollow)")),
            ("noopener", _("New tab security (noopener)")),
            ("noreferrer", _("Do not send referrer (noreferrer)")),
            ("ugc", _("User-generated content link (ugc)")),
            ("sponsored", _("Sponsored/Advertisement link (sponsored)")),
        ],
        required=False,
        label=_("Rel Attribute"),
        widget=forms.CheckboxSelectMultiple,
        help_text=_("If no option is selected, rel will remain empty (normal mode).")
    )

    address_list = forms.TypedChoiceField(
        choices=[],
        coerce=str,
        label=_('Site Pages List'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text=_("By selecting from the site pages list, the selected page address will be placed in the URL field.")
    )

    target_blank = forms.BooleanField(
        required=False,
        initial=False,
        label=_("Open in new tab")
    )

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

    # endregion
    class Meta:
        model = AdvText
        fields = ['title','section','url','address_list','target_blank','status','rel']

    def __init__(self, *args,request=None, **kwargs):

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        super().__init__(*args, **kwargs)

        dynamic_choices = [
            ('', '---------'),
        ]

        # page
        pages = Page.objects.filter(status="active",lang=self.lang).order_by('id')
        for page in pages:
            dynamic_choices.append((f'page_{page.id}', _("Page - %(title)s") % {'title': page.title}))

        # post
        posts = Post.objects.filter(status="published",lang=self.lang).order_by('id')
        for post in posts:
            dynamic_choices.append((f'post_{post.id}', _("Post - %(title)s") % {'title': post.title}))

        # section
        sections = Section.objects.filter(status="active",lang=self.lang).order_by('id')
        for section in sections:
            dynamic_choices.append((f'sec_{section.id}', _("Section - %(title)s") % {'title': section.title}))

        self.fields['address_list'].choices = dynamic_choices

        if self.instance and self.instance.pk and self.instance.rel:
            self.initial["rel"] = self.instance.rel.split()

        self.fields['section'].queryset = Section.objects.filter(
            status='active',
            type='post',
            lang=self.lang,
        )

    def clean_rel(self):
        values = self.cleaned_data.get("rel") or []
        return " ".join(values)


    def save(self, commit=True):
        """Save with automatic language setting."""
        instance = super().save(commit=False)
        instance.lang = self.lang

        if commit:
            instance.save()

        return instance


class AdvImageForm(forms.ModelForm):
    # region  field
    title = forms.CharField(
        label=_("Title"),
        max_length=60,
        error_messages={
            'required': _("Title is required."),
            'max_length': _("Title cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
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

    image = forms.ImageField(
        label=_("Image"),
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    url = forms.CharField(
        label=_('URL'),
        error_messages={
            'required': _("URL is required."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    rel = forms.MultipleChoiceField(
        choices=[
            ("nofollow", _("Do not pass SEO credit (nofollow)")),
            ("noopener", _("New tab security (noopener)")),
            ("noreferrer", _("Do not send referrer (noreferrer)")),
            ("ugc", _("User-generated content link (ugc)")),
            ("sponsored", _("Sponsored/Advertisement link (sponsored)")),
        ],
        required=False,
        label=_("Rel Attribute"),
        widget=forms.CheckboxSelectMultiple,
        help_text=_("If no option is selected, rel will remain empty (normal mode).")
    )

    address_list = forms.TypedChoiceField(
        choices=[],
        coerce=str,
        label=_('Site Pages List'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text=_("By selecting from the site pages list, the selected page address will be placed in the URL field.")
    )

    target_blank = forms.BooleanField(
        required=False,
        initial=False,
        label=_("Open in new tab")
    )

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

    # endregion
    class Meta:
        model = AdvImage
        fields = ['title','section','url','image','address_list','target_blank','status','rel']

    def __init__(self, *args, request=None, **kwargs):

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        super().__init__(*args, **kwargs)

        dynamic_choices = [
            ('', '---------'),
        ]

        # page
        pages = Page.objects.filter(status="active",lang=self.lang).order_by('id')
        for page in pages:
            dynamic_choices.append((f'page_{page.id}', _("Page - %(title)s") % {'title': page.title}))

        # post
        posts = Post.objects.filter(status="published",lang=self.lang).order_by('id')
        for post in posts:
            dynamic_choices.append((f'post_{post.id}', _("Post - %(title)s") % {'title': post.title}))

        # section
        sections = Section.objects.filter(status="active",lang=self.lang).order_by('id')
        for section in sections:
            dynamic_choices.append((f'sec_{section.id}', _("Section - %(title)s") % {'title': section.title}))

        self.fields['address_list'].choices = dynamic_choices

        self.fields['section'].queryset = Section.objects.filter(
            status='active',
            type='post',
            lang=self.lang,
        )

        if self.instance and self.instance.pk and self.instance.rel:
            self.initial["rel"] = self.instance.rel.split()

    def clean_rel(self):
        values = self.cleaned_data.get("rel") or []
        return " ".join(values)

    def save(self, commit=True):
        """Save with automatic language setting."""
        instance = super().save(commit=False)
        instance.lang = self.lang

        if commit:
            instance.save()

        return instance