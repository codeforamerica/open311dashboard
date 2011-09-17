from pymongo.connection import Connection
from django.template.defaultfilters import slugify

from dashboard.scripts.bounding_box import create_bounding_box
from dashboard.scripts.calculate_centroid import compute_centroid

from settings import MONGODB

connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]

def clean_up(filter = {}):
    """
    Clean up the raw SF street import.
    """

    streets = db.streets.find(filter)

    for street in streets:
        max_val = int(max([street['properties']['RT_TOADD'],
            street['properties']['LF_TOADD']]))
        min_val = int(min([street['properties']['RT_FADD'],
            street['properties']['LF_FADD']]))

        db.streets.update({ '_id' : street['_id']},
                { '$set' : { 'properties' : 
                    { 'name' : street['properties']['STREETN_GC'],
                        'right_range' : [
                            int(street['properties']['RT_FADD']),
                            int(street['properties']['RT_TOADD'])
                            ],
                        'left_range' : [
                            int(street['properties']['LF_FADD']),
                            int(street['properties']['LF_TOADD'])
                            ],
                        'min' : min_val,
                        'max' : max_val,
                        'type' : 'street',
                        'slug' : slugify(street['properties']['STREETN_GC'])
                        } } } )

def add_indexes():
    db.streets.ensure_index([( 'geometry.coordinates', '2d' )])

def find_centroid(filter = {}):
    """
    Find the centroids.
    """
    streets = db.streets.find(filter)

    for street in streets:
        centroid = compute_centroid(street['geometry']['coordinates'])
        db.streets.update({ '_id' : street['_id'] },
                { '$set' : { 'properties.centroid' : centroid }})

def find_bounding_box(filter = {}):
    """
    Find the bounding box.
    """
    streets = db.streets.find(filter)

    for street in streets:
        bbox = create_bounding_box(street['geometry']['coordinates'])
        db.streets.update({ '_id' : street['_id']},
                { '$set': { 'properties.bbox' : bbox }})

if __name__ == "__main__":
    clean_up()
    add_indexes()
    find_centroid()
    find_bounding_box()
