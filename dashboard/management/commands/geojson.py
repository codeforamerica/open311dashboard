from django.core.management.base import BaseCommand
from open311dashboard.dashboard.models import Geography, Request, Street

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
        cursor.execute("""
SELECT a.* FROM(
SELECT
	ST_AsGeoJSON(ST_Transform(ST_SetSRID(dashboard_street.line,900913),4326)),
	extract(epoch from avg(dashboard_request.updated_datetime - dashboard_request.requested_datetime)) as average,
	percent_rank() OVER (order by extract(epoch from avg(dashboard_request.updated_datetime - dashboard_request.requested_datetime))) as rank
FROM dashboard_street
LEFT OUTER JOIN
	dashboard_request ON (dashboard_street.id = dashboard_request.street_id)
WHERE
	dashboard_request.status='Closed' AND
	dashboard_request.updated_datetime > dashboard_request.requested_datetime AND
	requested_datetime > '2010-12-31' AND
	dashboard_request.service_code = '024'
GROUP BY dashboard_street.line
) AS a WHERE a.rank > .8
            """)
        rows = cursor.fetchall()

        for row in rows:
            geojson['features'].append({"type": "Feature",
                "geometry": json.loads(row[0]),
                "properties": {
                    "percentile": "%s" % row[2]
                    }})
        f = open('dashboard/static/sidewalk_cleaning.json', 'w')
        f.write(json.dumps(geojson))
        f.close()

        geojson['features'] = []

        cursor.execute("""
SELECT a.* FROM(
SELECT
	ST_AsGeoJSON(ST_Transform(ST_SetSRID(dashboard_street.line,900913),4326)),
	extract(epoch from avg(dashboard_request.updated_datetime - dashboard_request.requested_datetime)) as average,
	percent_rank() OVER (order by extract(epoch from avg(dashboard_request.updated_datetime - dashboard_request.requested_datetime))) as rank
FROM dashboard_street
LEFT OUTER JOIN
	dashboard_request ON (dashboard_street.id = dashboard_request.street_id)
WHERE
	dashboard_request.status='Closed' AND
	dashboard_request.updated_datetime > dashboard_request.requested_datetime AND
	requested_datetime > '2010-12-31' AND
	dashboard_request.service_code = '049'
GROUP BY dashboard_street.line
) AS a WHERE a.rank > .8
            """)
        rows = cursor.fetchall()
        for row in rows:
            geojson['features'].append({"type": "Feature",
                "geometry": json.loads(row[0]),
                "properties": {
                    "percentile": "%s" % row[2]
                    }})
        f = open('dashboard/static/graffiti.json', 'w')
        f.write(json.dumps(geojson))
        f.close()


        g = Geography.objects.all().transform()
        geojson['features'] = []

        for shape in g:
            geojson['features'].append({"type": "Feature",
                "geometry": json.loads(shape.geo.simplify(.0003,
                    preserve_topology=True).json),
                "properties": {
                    "neighborhood": shape.name
                    }})

        h = open('dashboard/static/neighborhoods.json', 'w')
        h.write(json.dumps(geojson))
        h.close()
