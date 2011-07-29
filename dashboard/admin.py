from django.contrib.gis import admin
from open311dashboard.dashboard.models import Geography, Street

admin.site.register(Geography, admin.OSMGeoAdmin)
admin.site.register(Street, admin.OSMGeoAdmin)
