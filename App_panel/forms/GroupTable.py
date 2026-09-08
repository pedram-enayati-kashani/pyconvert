from django import forms
from django.contrib.auth.models import Group
from ..models.Groups import GroupExtra
import re


class TableGroupForm(forms.Form):
    titles = forms.CharField(
        label='گروه‌ها',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def save(self):
        data = self.cleaned_data['titles']
        items = [i.strip() for i in re.split('[,،]', data) if i.strip()]

        created_groups = []

        for item in items:
            group = Group.objects.create(name=item.strip())
            GroupExtra.objects.create(
                group=group,
                status='active'
            )

            created_groups.append(group)

        return created_groups
