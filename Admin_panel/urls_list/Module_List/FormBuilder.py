from django.urls import path
from Admin_panel.views.Modules import FormBuilder

urlpatterns = [
    # Form
    path('', FormBuilder.Index.as_view(), name='form-builder'),
    path('create', FormBuilder.Create.as_view(), name='form-builder-create'),
    path('update/<int:pk>', FormBuilder.Update.as_view(), name='form-builder-update'),
    path('active/<int:pk>', FormBuilder.Active.as_view(), name='form-builder-active'),
    path('delete/<int:pk>',FormBuilder.Delete.as_view(), name='form-builder-delete'),
    path('filter/', FormBuilder.Query.as_view(), name='form-builder-query'),
    # Fields
    path('<int:pk>/field', FormBuilder.IndexField.as_view(), name='form-builder-field'),
    path('<int:pk>/field/create', FormBuilder.CreateField.as_view(), name='form-builder-field-create'),
    path('<int:pk>/field/update/<int:filed_pk>', FormBuilder.UpdateField.as_view(), name='form-builder-field-update'),
    path('<int:pk>/field/active/<int:filed_pk>', FormBuilder.ActiveField.as_view(), name='form-builder-field-active'),
    path('<int:pk>/field/delete/<int:filed_pk>',FormBuilder.DeleteField.as_view(), name='form-builder-field-delete'),
    # در urls.py
    path('<int:pk>/to-up/<int:filed_pk>', FormBuilder.ChangeFieldOrder.as_view(), {'direction': 'up'},name='form-builder-field-to-up'),
    path('<int:pk>/to-down/<int:filed_pk>', FormBuilder.ChangeFieldOrder.as_view(), {'direction': 'down'},name='form-builder-field-to-down'),

]