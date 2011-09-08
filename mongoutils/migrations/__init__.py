"""
Clean up the polygon metadata.
"""

from django.template.defaultfilters import slugify
from pymongo.connection import Connection

from settings import MONGODB

connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]

def build_slugs(collection, filters = {}):
    """
    Build the slugs for a set of GeoJSON features.
    """
    rows = db[collection].find(filters)

    for row in rows:
        db[collection].update({'_id' : row['_id']},
                { '$set' : { 'properties.slug' :
                   slugify(row['properties']['name']) }})

