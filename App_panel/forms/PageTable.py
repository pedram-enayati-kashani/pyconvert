import re
from django import forms
from App_panel.models.PageModel import Page

class TablePageForm(forms.Form):

    titles = forms.CharField(
        label='صفحه‌ها',
        help_text='مثال: درباره ما=about , تماس باما=contact',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def save(self):
        data = self.cleaned_data['titles']

        items = [i.strip() for i in re.split('[,،]', data) if i.strip()]

        pages = []

        for item in items:
            if '=' in item:
                title, slug = item.split('=', 1)
                title = title.strip()
                slug = slug.strip()
            else:
                title = item.strip()
                slug = None

            page = Page(
                title=title,
                slug=slug if slug else None
            )

            page.save()
            pages.append(page)

        return pages
