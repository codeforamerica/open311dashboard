from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'open311dashboard.dashboard.views.index'),
<<<<<<< HEAD
    url(r'^city/$', 'open311dashboard.dashboard.views.city'),
    url(r'^tickets/$', 'open311dashboard.dashboard.views.ticket_days'),
    url(r'^tickets/(?P<ticket_status>\w+)/$', 'open311dashboard.dashboard.views.ticket_days'),
    url(r'^tickets/(?P<ticket_status>\w+)/(?P<start>.+)/(?P<end>.+)/$', 'open311dashboard.dashboard.views.ticket_days'),
    # Examples:
    # url(r'^$', 'open311dashboard.views.home', name='home'),
    # url(r'^open311dashboard/', include('open311dashboard.foo.urls')),
=======
>>>>>>> ecfb19e07bc61da496f818387d76a52ed534b767

    # API Calls
    url(r'^api/tickets/$', 'open311dashboard.dashboard.views.ticket_days'),
    url(r'^api/tickets/(?P<ticket_status>opened|closed)/$',
        'open311dashboard.dashboard.views.ticket_days'),
    url(r'^api/tickets/(?P<ticket_status>opened|closed)/(?P<end>\d{4}-\d{2}-\d{2})/$',
        'open311dashboard.dashboard.views.ticket_days'),
    url(r'^api/tickets/(?P<ticket_status>opened|closed)/(?P<end>\d{4}-\d{2}-\d{2})/(?P<num_days>\d+)/',
        'open311dashboard.dashboard.views.ticket_days'),
    url(r'^api/tickets/(?P<ticket_status>opened|closed)/(?P<start>\d{4}-\d{2}-\d{2})/(?P<end>\d{4}-\d{2}-\d{2})/$',
        'open311dashboard.dashboard.views.ticket_days'),

    url(r'^api/more_info/(?P<begin>\d{4}-\d{2}-\d{2})/$',
        'open311dashboard.dashboard.views.ticket_day'),
    url(r'^api/more_info/(?P<begin>\d{4}-\d{2}-\d{2})/(?P<end>\d{4}-\d{2}-\d{2})/$',
        'open311dashboard.dashboard.views.ticket_day'),

    url(r'^api/list/(?P<begin>\d{4}-\d{2}-\d{2})/$',
        'open311dashboard.dashboard.views.list_requests'),
)
