from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('order/', include('order.urls', namespace='order')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
) + debug_toolbar_urls()


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = 'Tea Shop Admin'
admin.site.index_title = 'Tea Shop'