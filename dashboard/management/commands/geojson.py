from django.core.management.base import BaseCommand

from django.db import connection
from optparse import make_option
import json

class Command(BaseCommand):
    # option_list = BaseCommand.option_list + (
            # make_option('--directory', dest='directory',
                # default='dashboard/static/geojson/',
                # help="default directory to save tiles to")
            # )
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
        for row in rows:
            geojson1['features'].append({"type": "Feature",
                "geometry": json.loads(row[1]),
                "properties": {
                    "average": row[0]
                    }})
        f = open('dashboard/static/test.json', 'w')
        f.write(json.dumps(geojson1))


        cursor.execute("""SELECT
        ST_AsGeoJson(ST_simplify(ST_Transform(ST_SetSRID(geo, 900913), 4326),
        0.0005)), name FROM dashboard_geography""")
        rows = cursor.fetchall()
        for row in rows:
            geojson['features'].append({"type": "Feature",
                "geometry": json.loads(row[0]),
                "properties": {
                    "name": row[1]
                }})
        f = open('dashboard/static/neighborhoods.json', 'w')
        f.write(json.dumps(geojson))
