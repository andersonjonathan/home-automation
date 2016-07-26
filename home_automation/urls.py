from django.conf.urls import include, url
from django.contrib import admin
from wired.views import login#, index, switch,
from django.contrib.auth.views import logout

urlpatterns = [
    # Examples:
    # url(r'^$', 'home_automation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', view=index, name="index"),
    # url(r'^api/switch/(?P<pk>[0-9]+)/(?P<button_pk>[^/]+)/$', view=switch, name="switch"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, {'template_name': 'wired/login.html'}),
    url(r'^accounts/logout/$', logout),
]
