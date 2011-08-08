from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'open311dashboard.dashboard.views.index'),
    url(r'^map/$', 'open311dashboard.dashboard.views.map'),
    url(r'^street/$', 'open311dashboard.dashboard.views.street_list'),
    url(r'^street/(?P<street_id>\d+)/$',
        'open311dashboard.dashboard.views.street_view'),

    # Login
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),

    # API Calls
    url(r'^api/tickets/$', 'open311dashboard.dashboard.views.ticket_days'),
    url(r'^api/tickets/(?P<ticket_status>open|closed|both)/$',
        'open311dashboard.dashboard.views.ticket_days'),
    url(r'^api/tickets/(?P<ticket_status>open|closed|both)/(?P<num_days>\d+)/$',
        'open311dashboard.dashboard.views.ticket_days'),
    url(r'^api/tickets/(?P<ticket_status>open|closed|both)/(?P<end>\d{4}-\d{2}-\d{2})/$',
        'open311dashboard.dashboard.views.ticket_days'),
    url(r'^api/tickets/(?P<ticket_status>open|closed|both)/(?P<end>\d{4}-\d{2}-\d{2})/(?P<num_days>\d+)/',
        'open311dashboard.dashboard.views.ticket_days'),
    url(r'^api/tickets/(?P<ticket_status>open|closed|both)/(?P<start>\d{4}-\d{2}-\d{2})/(?P<end>\d{4}-\d{2}-\d{2})/$',
        'open311dashboard.dashboard.views.ticket_days'),

    # More in depth aggregate data.
    url(r'^api/more_info/(?P<begin>\d{4}-\d{2}-\d{2})/$',
        'open311dashboard.dashboard.views.ticket_day'),
    url(r'^api/more_info/(?P<begin>\d{4}-\d{2}-\d{2})/(?P<end>\d{4}-\d{2}-\d{2})/$',
        'open311dashboard.dashboard.views.ticket_day'),

    # All tickets within a range of dates.
    url(r'^api/list/(?P<begin>\d{4}-\d{2}-\d{2})/$',
        'open311dashboard.dashboard.views.list_requests'),
    url(r'^api/list/(?P<begin>\d{4}-\d{2}-\d{2})/(?P<end>\d{4}-\d{2}-\d{2})/$',
        'open311dashboard.dashboard.views.list_requests'),

    # Handle admin stuff.
    url(r'^admin/$', 'open311dashboard.dashboard.views.admin'),
    url(r'^admin/(?P<shortname>\w+)/$',
        'open311dashboard.dashboard.views.city_admin'),
    url(r'^admin/new/$', 'open311dashboard.dashboard.views.city_add'),
)
