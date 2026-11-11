from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from module.models.MenuBuilder import Menu, Menu_Links
from App_panel.models.PostModel import Post
from App_panel.models.PageModel import Page
from App_panel.models.CategoriesModel import Category
from App_panel.models.TagModel import Tag
from App_panel.models.SectionModel import Section
from Admin_panel.helpers.module.menu_builder import build_url_from_target


class MenuBuilderForm(forms.ModelForm):
    # region  field
    title = forms.CharField(
        label=_('Title'),
        max_length=120,
        error_messages={
            'required': _("Title is required."),
            'max_length': _("Title cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    name = forms.CharField(
        label=_('Name'),
        max_length=60,
        error_messages={
            'required': _("Name is required."),
            'max_length': _("Name cannot be more than %(limit_value)d characters."),
        },
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9]+(_[A-Za-z0-9]+)*$',
                message=_("The value was not entered correctly!"),
            )
        ],
        help_text=_('Only English letters, no spaces, and separate words with "_". Example: first_text'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    status = forms.TypedChoiceField(
        choices=[
            ('active', _("Active")),
            ('inactive', _("Inactive")),
        ],
        coerce=str,
        initial='active',
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # endregion
    class Meta:
        model = Menu
        fields = ['title', 'name', 'status']

    def __init__(self, *args, request=None, **kwargs):

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        super().__init__(*args, **kwargs)


    def save(self, commit=True):
        """Save with automatic language setting."""
        instance = super().save(commit=False)
        instance.lang = self.lang

        if commit:
            instance.save()

        return instance


class LinkForm(forms.ModelForm):
    # region  field
    title = forms.CharField(
        label=_('Title'),
        max_length=120,
        error_messages={
            'required': _("Title is required."),
            'max_length': _("Title cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    name = forms.CharField(
        label=_('Name'),
        max_length=60,
        error_messages={
            'required': _("Name is required."),
            'max_length': _("Name cannot be more than %(limit_value)d characters."),
        },
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]+(_[A-Za-z]+)*$',
                message=_("The value was not entered correctly!"),
            )
        ],
        help_text=_('Only English letters, no spaces, and separate words with "_". Example: first_text'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    url = forms.CharField(
        label=_('URL'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=_('If this is an external link, enter the URL. Otherwise, select the target from the list.'),
    )

    parent = forms.ModelChoiceField(
        queryset=Menu_Links.objects.filter(status='active'),
        label=_('Parent Link'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    address_list = forms.TypedChoiceField(
        choices=[],
        coerce=str,
        label=_('Site Pages List'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text=_("By selecting from the site pages list, the selected page address will be placed in the URL field.")
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

    target_blank = forms.BooleanField(
        required=False,
        initial=False,
        label=_("Open in new tab")
    )

    status = forms.TypedChoiceField(
        choices=[
            ('active', _("Active")),
            ('inactive', _("Inactive")),
        ],
        coerce=str,
        initial='active',
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # endregion
    class Meta:
        model = Menu_Links
        fields = ['title', 'name', 'url', 'parent', 'address_list', 'rel', 'target_blank', 'status']

    def __init__(self, *args,request=None, **kwargs):

        if request and getattr(request, 'LANGUAGE_CODE', None):
            self.lang = request.LANGUAGE_CODE
        else:
            self.lang = translation.get_language() or 'fa'

        super().__init__(*args, **kwargs)

        # parent
        parent_qs = Menu_Links.objects.filter(status='active')

        if self.instance and self.instance.pk:
            parent_qs = parent_qs.exclude(pk=self.instance.pk)

        self.fields['parent'].queryset = parent_qs

        # region  target
        dynamic_choices = [
            ('', '---------'),
        ]

        # page
        pages = Page.objects.filter(status="active").order_by('id')
        for page in pages:
            dynamic_choices.append((f'page_{page.id}', _("Page - %(title)s") % {'title': page.title}))

        # category
        categories = Category.objects.filter(status="published").order_by('id')
        for category in categories:
            dynamic_choices.append((f'cate_{category.id}', _("Category - %(title)s") % {'title': category.title}))

        # section
        sections = Section.objects.filter(status="active", type__in=['post', 'no_post']).order_by('id')
        for section in sections:
            dynamic_choices.append((f'sec_{section.id}', _("Section - %(title)s") % {'title': section.title}))

        # sitemap and robots
        dynamic_choices.append(("robots", "Robots.txt"))
        dynamic_choices.append(("sitemap", "Sitemap.xml"))

        self.fields['address_list'].choices = dynamic_choices
        # endregion

        # rel
        if self.instance and self.instance.pk and self.instance.rel:
            self.initial["rel"] = self.instance.rel.split()

    def save(self, commit=True):
        """Save with automatic language setting."""
        instance = super().save(commit=False)
        instance.lang = self.lang

        if commit:
            instance.save()

        return instance

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        address_list = cleaned_data.get("address_list")

        if address_list:
            generated_url = build_url_from_target(address_list)
            if not generated_url:
                raise forms.ValidationError(_("A valid URL could not be generated for the selected page."))
            cleaned_data["url"] = generated_url
            return cleaned_data

        if not url:
            raise forms.ValidationError(_("Either enter a URL or select one from the site pages list."))

        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = self._meta.model.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(_("This name already exists."))

        return name

    def clean_rel(self):
        values = self.cleaned_data.get("rel") or []
        return " ".join(values)