from django import forms
from django.contrib.auth.models import Group, Permission
from ..models import GroupExtra


class GroupForm(forms.ModelForm):

    status = forms.ChoiceField(
        choices=GroupExtra.STATUS_CHOICES,
        label='وضعیت',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        label='دسترسی‌ها',
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control selectGroup'}
        )
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions', 'status']

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'}
            )
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # حالت ویرایش
        if self.instance.pk:

            try:
                self.fields['status'].initial = self.instance.extra.status

            except GroupExtra.DoesNotExist:
                self.fields['status'].initial = 'active'

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
            self.save_m2m()
            extra, created = GroupExtra.objects.get_or_create(
                group=group
            )
            extra.status = self.cleaned_data['status']
            extra.save()

        return group

