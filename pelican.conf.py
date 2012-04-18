# -*- coding: utf-8 -*-
AUTHOR = u'Juan José Denis Corrales'
SITENAME = u"Axaragua Fotoblog"
SITEURL = 'http://jjdenis.github.com'
TIMEZONE = "Europe/Madrid"

GITHUB_URL = 'http://github.com/jjdenis/'
#DISQUS_SITENAME = "blog-notmyidea"
PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = True
LOCALE = "es_ES"
DEFAULT_PAGINATION = 4

THEME = '/Users/jjdenis/jjdenis.github.com/notmyideatuneado'

FEED_RSS = 'feeds/all.rss.xml'
#CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
FEED_DOMAIN = SITEURL
FEED_MAX_ITEMS = 20


'''
LINKS = (('Biologeek', 'http://biologeek.org'),
         ('Filyb', "http://filyb.info/"),
         ('Libert-fr', "http://www.libert-fr.com"),
         ('N1k0', "http://prendreuncafe.com/blog/"),
         (u'Tarek Ziadé', "http://ziade.org/blog"),
         ('Zubin Mithra', "http://zubin71.wordpress.com/"),)

SOCIAL = (('twitter', 'http://twitter.com/ametaireau'),
          ('lastfm', 'http://lastfm.com/user/akounet'),
          ('github', 'http://github.com/ametaireau'),)

SOCIAL = (
          ('github', 'http://github.com/ametaireau'),)


'''

SOCIAL = (
          ('github', 'http://github.com/jjdenis'),)


# global metadata to all the contents
DEFAULT_METADATA = (('yeah', 'it is'),)

# static paths will be copied under the same name
STATIC_PATHS = ["pictures", "imagenes"]

# A list of files to copy from the source to the destination
FILES_TO_COPY = (('extra/robots.txt', 'robots.txt'),)

# foobar will not be used, because it's not in caps. All configuration keys
# have to be in caps
foobar = "barbaz"
