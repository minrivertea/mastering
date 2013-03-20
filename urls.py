from django.conf.urls.defaults import *
from django.conf import settings
import django.views.static
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.views.generic.simple import direct_to_template
from shop.models import Product

# admin urls
from django.contrib import admin
admin.autodiscover()

# for the sitemaps
products = {
    'queryset': Product.objects.filter(is_active=True),
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'products': GenericSitemap(products, priority=0.6),
}


# main URL patterns
urlpatterns = patterns('',
    (r'^', include('mastering.shop.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^captcha/', include('captcha.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^humans\.txt$', direct_to_template, {'template': 'humans.txt', 'mimetype': 'text/plain'}),
    (r'^products\.xml$', direct_to_template, {'template': 'products.xml', 'mimetype': 'text/xml'}),
    (r'^404/$', direct_to_template, {'template': '404.html'}), 
    (r'^500/$', direct_to_template, {'template': '500.html'}),    
)


# for the development server static files
urlpatterns += patterns('',

    # CSS, Javascript and IMages
    (r'^images/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/images',
        'show_indexes': settings.DEBUG}),
    (r'^cache/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/cache',
        'show_indexes': settings.DEBUG}),
    (r'^thumbs/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/thumbs',
        'show_indexes': settings.DEBUG}),
    (r'^css/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/css',
        'show_indexes': settings.DEBUG}),
    (r'^js/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/js',
        'show_indexes': settings.DEBUG}),
)
