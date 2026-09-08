from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include, re_path
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap, index
from Admin_panel.views.sitemap import PostSitemap, CategorySitemap, TagSitemap, SectionSitemap, PagesSitemap
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

sitemaps = {
    'pages': PagesSitemap,
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap,
    'sections': SectionSitemap,
}

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('app/', include("App_panel.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("captcha/", include("captcha.urls")),
]

urlpatterns += i18n_patterns(
path('admin/', include('Admin_panel.urls')),
    path('', include("Client.urls")),
    path('sitemap.xml', index, {'sitemaps': sitemaps}, name='sitemap'),
    path('<section>-sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
)

if settings.SERVE_STATIC_LOCAL:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

handler404 = 'Client.views.index.custom_404_view'
