from django.contrib.sitemaps import Sitemap
from blog.models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.dt_updated
