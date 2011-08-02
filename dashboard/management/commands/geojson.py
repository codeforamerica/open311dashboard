from django.core.management.base import BaseCommand
from open311dashboard.dashboard.models import Geography

from django.db import connection
import json

# TODO: ABSTRACT THIS!
class Command(BaseCommand):
    help = """

    Grab relevant GeoJSON files to store and interact with the maps layer. We
    do not do this dynamically because the map layers are generated once a week
    and the JSON overlay should not interfere

    """

    def handle(self, *args, **options):
        geojson = {"type": "FeatureCollection",
                "features":[]
                }
        # Select JSON

        cursor = connection.cursor()
        cursor.execute("""SELECT extract(epoch from
            avg(dashboard_request.updated_datetime -
                dashboard_request.requested_datetime))/3600 as average,
            ST_AsGeoJSON(transform(ST_SetSRID(dashboard_street.line, 900913),4326)) FROM dashboard_request,
            dashboard_street WHERE dashboard_request.status='Closed' AND
            dashboard_request.street_id=dashboard_street.id AND
            dashboard_request.updated_datetime >
            dashboard_request.requested_datetime AND requested_datetime >
            '2010-12-31' GROUP BY dashboard_street.line ORDER BY average DESC LIMIT 2000
            """)
        rows = cursor.fetchall()

        geojson1 = geojson
        geojson2 = geojson
        for row in rows:
            geojson1['features'].append({"type": "Feature",
                "geometry": json.loads(row[1]),
                "properties": {
                    "average": row[0]
                    }})
        f = open('dashboard/static/test.json', 'w')
        f.write(json.dumps(geojson1))
        f.close()

        g = Geography.objects.all().transform()
        geojson2['features'] = []

        for shape in g:
            geojson2['features'].append({"type": "Feature",
                "geometry": json.loads(shape.geo.simplify(.0003,
                    preserve_topology=True).json),
                "properties": {
                    "neighborhood": shape.name
                    }})

        h = open('dashboard/static/neighborhoods.json', 'w')
        h.write(json.dumps(geojson2))
        h.close()
