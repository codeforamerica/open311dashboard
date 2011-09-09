from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'dashboard.views.index'),
    url(r'^map/$', 'dashboard.views.map'),

    url(r'^street/$', 'dashboard.views.street_list'),
    url(r'^street/(?P<street_name>.+)/(?P<min_val>\d+)-(?P<max_val>\d+)/$',
        'dashboard.views.street_view'),
    # Needs to be below for proper URL matching.
    url(r'^street/(?P<street_name>.+)/$',
        'dashboard.views.street_specific_list'),

    url(r'^neighborhood/$',
        'dashboard.views.neighborhood_list'),
    url(r'^neighborhood/(?P<neighborhood_slug>.+)/$',
        'dashboard.views.neighborhood_detail'),
    # url(r'^neighborhood/(?P<neighborhood_id>\d+).json$',
        # 'dashboard.views.neighborhood_detail_json'),

    url(r'^search/$',
        'dashboard.views.street_search'),

    # API Calls
    url(r'^api/home/(?P<geography>\d+).json$',
        'dashboard.views.index', {'is_json': True}),

)
