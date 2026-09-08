from django.urls import path
from Admin_panel.views.Modules import redirect_rule

urlpatterns = [
    # Form
    path('', redirect_rule.Index.as_view(), name='redirect'),
    path('create', redirect_rule.Create.as_view(), name='redirect-create'),
    path('update/<int:pk>', redirect_rule.Update.as_view(), name='redirect-update'),
    path('active/<int:pk>', redirect_rule.Active.as_view(), name='redirect-active'),
    path('delete/<int:pk>', redirect_rule.Delete.as_view(), name='redirect-delete'),
    path('filter/', redirect_rule.Query.as_view(), name='redirect-query'),
]