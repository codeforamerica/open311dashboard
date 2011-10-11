"""
Mongo helper methods for request data.
"""
import re

from pymongo.connection import Connection

from settings import MONGODB
from dashboard.scripts import nearest_street

connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]

def add_indexes():
    db.requests.ensure_index([('coordinates', '2d')])

def drop_indexes():
    db.requests.drop_indexes()

def find_nearest_street(coordinate_list, max_distance):
    """
    Find the nearest street.
    """
    streets = db.streets.find({ 'geometry.coordinates': {'$within':
            { '$center' : [coordinate_list, max_distance]}}})
    xy_coords = nearest_street.lat_long_to_x_y_list(coordinate_list)
    distance = 400

    for street in streets:
        # Loop through each street and convert it to x,y.
        xy_line = []
        print street['properties']['name']

        for coordinate_point in street['geometry']['coordinates']:
            xy_point = nearest_street. \
                lat_long_to_x_y_list(coordinate_point)
            xy_line.append(xy_point)

        # Loop in here.
        for i in range(len(xy_line)-1):
            computed_distance = nearest_street.compute_distance(
                    xy_coords, xy_line[i], xy_line[i+1])

            if (distance > computed_distance):
                distance = computed_distance
                street_id = street['_id']

        return street_id

def update_nearest_streets(filter_requests={}, max_distance=.005):
    """
    Find the nearest street to each request in a queryset.
    """

    requests = db.requests.find(filter_requests)

    for request in requests:
        print request['service_request_id']
        street_id = find_nearest_street(request['coordinates'], max_distance)
        db.requests.update({'_id' : request['_id']},
                { '$set' : {'street' : street_id }})


if __name__ == '__main__':
    add_indexes()
    update_nearest_streets()

