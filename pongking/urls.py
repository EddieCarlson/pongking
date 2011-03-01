from django.conf.urls.defaults import *
import os

from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

doc_root = os.path.join(settings.BASE_PATH, 'static')
urlpatterns = patterns('',
	
	(r'^$', 'pongking.pong.views.loginpage'),
	(r'^addplayer/$', 'pongking.pong.views.addPlayer'),
	(r'^navbar/$', 'pongking.pong.views.navbar'),
	(r'^addgame/$', 'pongking.pong.views.addGame'),
	(r'^mobilemenu/$', 'pongking.pong.views.mobileMenu'),
	(r'^mobilerank/$', 'pongking.pong.views.mobileRank'),
	(r'^addgamemobile/$', 'pongking.pong.views.addGameMobile'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     	{'document_root': doc_root}),

    # Example:
    # (r'^pongking/', include('pongking.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
