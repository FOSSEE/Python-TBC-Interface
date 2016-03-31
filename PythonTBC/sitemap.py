from django.contrib.sitemaps import Sitemap
from tbc.models import Chapters

class TbcBookSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Chapters.objects.all()
