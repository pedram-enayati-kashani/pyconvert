from django_ckeditor_5.widgets import CKEditor5Widget
import json
from .middleware import get_current_language


class DynamicCKEditorWidget(CKEditor5Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_name = 'default'

    def render(self, name, value, attrs=None, renderer=None):
        self.editor_language = get_current_language()
        is_fa = self.editor_language.startswith('fa')
        direction = 'rtl' if is_fa else 'ltr'
        language_code = 'fa' if is_fa else 'en'

        self.config = {
            'toolbar': [
                'heading', '|',
                'bold', 'italic', 'link',
                'bulletedList', 'numberedList', '|',
                'fontColor', 'fontBackgroundColor', '|',
                'imageUpload', 'blockQuote', 'undo', 'redo', '|',
                'insertTable', 'tableColumn', 'tableRow', 'mergeTableCells', '|',
                'sourceEditing', '|',
                'removeFormat'
            ],
            'language': {
                'ui': language_code,
                'content': language_code,
                'textPartLanguage': language_code
            },
            'table': {
                'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells'],
                'tableProperties': {
                    'borderColors': ['white', 'black', '#007bff', '#dc3545'],
                    'backgroundColors': ['white', 'yellow', '#d4edda', '#f8d7da']
                }
            },
            'fontColor': {
                'colors': [
                    {'color': '#000000', 'label': 'Black'},
                    {'color': '#434343', 'label': 'Dark Gray'},
                    {'color': '#666666', 'label': 'Gray'},
                    {'color': '#999999', 'label': 'Light Gray'},
                    {'color': '#B7B7B7', 'label': 'Silver'},
                    {'color': '#CCCCCC', 'label': 'Silver Gray'},
                    {'color': '#EFEFEF', 'label': 'White Smoke'},
                    {'color': '#FFFFFF', 'label': 'White'},
                    {'color': '#FF0000', 'label': 'Red'},
                    {'color': '#FF9900', 'label': 'Orange'},
                    {'color': '#FFFF00', 'label': 'Yellow'},
                    {'color': '#00FF00', 'label': 'Lime'},
                    {'color': '#00FFFF', 'label': 'Cyan'},
                    {'color': '#0000FF', 'label': 'Blue'},
                    {'color': '#FF00FF', 'label': 'Magenta'},
                    {'color': '#990000', 'label': 'Dark Red'},
                    {'color': '#FF6600', 'label': 'Dark Orange'},
                    {'color': '#999900', 'label': 'Dark Yellow'},
                    {'color': '#009900', 'label': 'Dark Green'},
                    {'color': '#009999', 'label': 'Dark Cyan'},
                    {'color': '#000099', 'label': 'Dark Blue'},
                    {'color': '#990099', 'label': 'Dark Magenta'},
                    {'color': '#FF99CC', 'label': 'Pink'},
                    {'color': '#CC99FF', 'label': 'Plum'},
                    {'color': '#99CCFF', 'label': 'Light Blue'},
                    {'color': '#99FF99', 'label': 'Light Green'},
                    {'color': '#FFFF99', 'label': 'Light Yellow'},
                    {'color': '#FFCC99', 'label': 'Peach'},
                    {'color': '#800000', 'label': 'Maroon'},
                    {'color': '#808000', 'label': 'Olive'},
                    {'color': '#008000', 'label': 'Green'},
                    {'color': '#008080', 'label': 'Teal'},
                    {'color': '#000080', 'label': 'Navy'},
                    {'color': '#800080', 'label': 'Purple'},
                    {'color': '#808080', 'label': 'Gray'},
                    {'color': '#C0C0C0', 'label': 'Silver'},
                ],
                'documentColors': 10
            },
            'fontBackgroundColor': {
                'colors': [
                    {'color': '#000000', 'label': 'Black'},
                    {'color': '#434343', 'label': 'Dark Gray'},
                    {'color': '#666666', 'label': 'Gray'},
                    {'color': '#999999', 'label': 'Light Gray'},
                    {'color': '#B7B7B7', 'label': 'Silver'},
                    {'color': '#CCCCCC', 'label': 'Silver Gray'},
                    {'color': '#EFEFEF', 'label': 'White Smoke'},
                    {'color': '#FFFFFF', 'label': 'White'},
                    {'color': '#FF0000', 'label': 'Red'},
                    {'color': '#FF9900', 'label': 'Orange'},
                    {'color': '#FFFF00', 'label': 'Yellow'},
                    {'color': '#00FF00', 'label': 'Lime'},
                    {'color': '#00FFFF', 'label': 'Cyan'},
                    {'color': '#0000FF', 'label': 'Blue'},
                    {'color': '#FF00FF', 'label': 'Magenta'},
                    {'color': '#990000', 'label': 'Dark Red'},
                    {'color': '#FF6600', 'label': 'Dark Orange'},
                    {'color': '#999900', 'label': 'Dark Yellow'},
                    {'color': '#009900', 'label': 'Dark Green'},
                    {'color': '#009999', 'label': 'Dark Cyan'},
                    {'color': '#000099', 'label': 'Dark Blue'},
                    {'color': '#990099', 'label': 'Dark Magenta'},
                    {'color': '#FF99CC', 'label': 'Pink'},
                    {'color': '#CC99FF', 'label': 'Plum'},
                    {'color': '#99CCFF', 'label': 'Light Blue'},
                    {'color': '#99FF99', 'label': 'Light Green'},
                    {'color': '#FFFF99', 'label': 'Light Yellow'},
                    {'color': '#FFCC99', 'label': 'Peach'},
                    {'color': '#800000', 'label': 'Maroon'},
                    {'color': '#808000', 'label': 'Olive'},
                    {'color': '#008000', 'label': 'Green'},
                    {'color': '#008080', 'label': 'Teal'},
                    {'color': '#000080', 'label': 'Navy'},
                    {'color': '#800080', 'label': 'Purple'},
                    {'color': '#808080', 'label': 'Gray'},
                    {'color': '#C0C0C0', 'label': 'Silver'},
                ],
                'documentColors': 10  # نمایش ۱۰ رنگ اخیر استفاده شده
            }
        }

        self.attrs.update({
            'data-language': language_code,
            'data-direction': direction,
            'lang': language_code,
            'dir': direction,
            'data-ckeditor-config': json.dumps(self.config)
        })

        return super().render(name, value, attrs, renderer)