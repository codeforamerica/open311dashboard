from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'open311dashboard.dashboard.views.index'),
    url(r'^map/$', 'open311dashboard.dashboard.views.map'),

    url(r'^street/$', 'open311dashboard.dashboard.views.street_list'),
    url(r'^street/(?P<street_id>\d+)/$',
        'open311dashboard.dashboard.views.street_view'),
    url(r'^street/(?P<street_id>\d+).json',
        'open311dashboard.dashboard.views.street_view_json'),

    url(r'^neighborhood/$',
        'open311dashboard.dashboard.views.neighborhood_list'),
    url(r'^neighborhood/(?P<neighborhood_id>\d+)/$',
        'open311dashboard.dashboard.views.neighborhood_detail'),
    url(r'^neighborhood/(?P<neighborhood_id>\d+).json$',
        'open311dashboard.dashboard.views.neighborhood_detail_json'),

    url(r'^search/$',
        'open311dashboard.dashboard.views.street_search'),

    # Login
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),

    # API Calls
    url(r'^api/home/(?P<geography>\d+).json$',
        'open311dashboard.dashboard.views.index', {'is_json':True}),

    # Handle admin stuff.
    url(r'^admin/$', 'open311dashboard.dashboard.views.admin'),
    url(r'^admin/(?P<shortname>\w+)/$',
        'open311dashboard.dashboard.views.city_admin'),
    url(r'^admin/new/$', 'open311dashboard.dashboard.views.city_add'),
)
