from django.conf.urls import patterns, include, url
import tbc_error_page.views
import commentingapp.views
import django.contrib.sitemaps.views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from .sitemap import TbcBookSitemap
sitemaps = { 
    'book': TbcBookSitemap, 
}

urlpatterns = [
    # Examples:
    # url(r'^$', 'PythonTBC.views.home', name='home'),
    # url(r'^PythonTBC/', include('PythonTBC.foo.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin', include(admin.site.urls)),
    url(r'^', include('tbc.urls', namespace='tbc')),
    url(r'^sitemap\.xml$', django.contrib.sitemaps.views.sitemap, {'sitemaps': sitemaps}),

    url(r'^admin-tools/commenting', commentingapp.views.commenting, name = 'commenting'),
    url(r'^admin-tools/error_page', tbc_error_page.views.error, name = 'error_page'),
    url(r'^admin-tools/broken_page', tbc_error_page.views.broken, name = 'broken_page'),
   

]

