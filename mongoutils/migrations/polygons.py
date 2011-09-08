from pymongo.connection import Connection
from django.template.defaultfilters import slugify

from settings import MONGODB

connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]

def clean_up(filter = {}):
    """
    Clean up the raw SF polygon import.
    """

    polygons = db.polygons.find(filter)

    for polygon in polygons:

        db.polygons.update({ '_id' : polygon['_id']},
                { '$set' : { 'properties' : 
                    { 'name' : polygon['properties']['NBRHOOD'],
                        'type' : 'neighborhood',
                        'slug' : slugify(polygon['properties']['NBRHOOD'])
                        } } } )

def add_indexes():
    db.polygons.ensure_index([('geometry.coordinates.0', '2d')])

if __name__ == "__main__":
    clean_up()
    add_indexes()
