"""sitemap.py
A sitemap is an XML file on your website that tells search-engine
indexers how frequently your pages change and how 'important' certain
pages are in relation to other pages on your site. This information
helps search engines index your site.

The Django sitemap framework automates the creation of this XML file by
letting you express this information in Python code.

It works much like Djangos syndication framework. To create a sitemap,
just write a Sitemap class and point to it in your URLconf.
"""
from django.contrib.sitemaps import Sitemap
from tbc.models import Chapters


class TbcBookSitemap(Sitemap):
    """class TbcBookSitemap
    class with one argument
    """
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Chapters.objects.all()
