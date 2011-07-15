from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import views


urlpatterns = patterns('',
    url(r'^$', views.index, name="home"),
    url(r'^contact-us/$', views.contact_us, name="contact_us"),
    url(r'^news/$', views.all_news, name="all_news"),
    url(r'^news/(?P<slug>[\w-]+)/$', views.news_item, name="news_item"),
    url(r'^manufacturer/(?P<cat>[\w-]+)/$', views.category, name="category"),
    url(r'^manufacturer/(?P<cat>[\w-]+)/(?P<sub_cat>[\w-]+)/$', views.sub_category, name="sub_category"),
    url(r'^china-manufacturer/(?P<slug>[\w-]+)/$', views.product, name="product"),
    url(r'^create_products/$', views.create_products, name="create_products"),
)

