from django.contrib.gis import admin
from open311dashboard.dashboard.models import Neighborhoods

admin.site.register(Neighborhoods, admin.OSMGeoAdmin)
