from django import forms
from django.core import validators
from django_ckeditor_5.widgets import CKEditor5Widget
from django.utils.translation import gettext_lazy as _
from App_panel.models.UsersModel import Users

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label= _("First Name"),
        max_length=30,
        error_messages={
            'required': _("First Name is required."),
            'max_length': _("First Name cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    last_name = forms.CharField(
        label= _("Last Name"),
        max_length=40,
        error_messages={
            'required': _("Last Name is required."),
            'max_length': _("Last Name cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    summery = forms.CharField(
        label= _("summary"),
        max_length=200,
        required=False,
        error_messages={
            'max_length': _("Summary cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description_seo = forms.CharField(
        label= _("Meta description"),
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

    description = forms.CharField(
        label= _("Description"),
        required=False,
        widget=CKEditor5Widget(config_name='default'),
    )

    mobile = forms.CharField(
        label=_('Mobile number'),
        required=False,
        max_length=15,
        error_messages={
            'max_length': _("Mobile number cannot be more than %(limit_value)d characters."),
        },
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    display_name = forms.ChoiceField(
        label=_('Display name format'),
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    avatar = forms.ImageField(
        label=_('Profile picture'),
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'summery', 'description_seo','description','mobile','display_name','avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.first_name and user.last_name:
            self.fields['display_name'].choices = [
                ('username', user.username),
                ('first_last', f"{user.first_name} {user.last_name}".strip()),
                ('last_first', f"{user.last_name} {user.first_name}".strip()),
            ]
        else:
            self.fields['display_name'].choices = [
                ('username', user.username),
            ]

    def clean_description(self):
        description = self.cleaned_data.get('description', '')

        if not description:
            return description
        pattern = r'<h[1-6](\s[^>]*)?>(\s|&nbsp;|<br\s*/?>)*</h[1-6]>'
        max_iterations = 5
        for _ in range(max_iterations):
            new_description = re.sub(
                pattern,
                '<p>&nbsp;</p>',
                description,
                flags=re.IGNORECASE
            )
            if new_description == description:
                break
            description = new_description

        return description

class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(
        label=_('Old Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    password = forms.CharField(
        label=_('New Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    confirm_password = forms.CharField(
        label=_('Confirm New Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )