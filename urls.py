from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'open311dashboard.dashboard.views.index'),

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
)
