from django.urls import path
from App_panel.views import Tables

urlpatterns = [
    path('', Tables.Index.as_view(), name='table'),
    path('page/create', Tables.PageCreate.as_view(), name='table-page-create'),
    path('section', Tables.SectionIndex.as_view(), name='table-section'),
    path('section/create', Tables.SectionCreate.as_view(), name='table-section-create'),
    path('section/update/<int:pk>', Tables.SectionUpdate.as_view(), name='table-section-update'),
    path('group/create', Tables.GroupCreate.as_view(), name='table-group-create'),
    path('module/create', Tables.ModuleCreate.as_view(), name='table-module-create'),
    path("backup/sqlite", Tables.BaseExportView.as_view(), name="table-backup-sqlite"),
    path("backup/mysql", Tables.ExportMySQLView.as_view(), name="table-backup-mysql"),
    path("backup/postgres", Tables.ExportPostgresView.as_view(), name="table-backup-postgres"),
    path("input/postgres", Tables.InputPostgresSqlListView.as_view(), name="table-input-postgres"),
    path("input/postgres/<str:app_label>/<str:model_name>",Tables.InputPostgresSqlDetailView.as_view(),name="table-input-detail"),
    path("input/postgres/query",Tables.InputPostgresQueryView.as_view(),name="table-input-query"),
]