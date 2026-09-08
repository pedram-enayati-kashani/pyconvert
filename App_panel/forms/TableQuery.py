from django import forms

class SQLImportForm(forms.Form):
    sql_queries = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 20,
            'class': 'form-control',
            'placeholder': 'دستورات SQL (INSERT INTO...) را اینجا پیست کنید...'
        }),
        label="دستورات SQL"
    )