#!/usr/bin/python
"""
Mashing 311 incident data with San Francisco street centerlines
Calculating average response times for each block in San Francisco
"""
import urllib
import json as simplejson
import pprint
import math

service_requests_url = 'input/service_requests_response_times.json'
centerlines_url = 'input/centerlines.json'

def lat_long_to_x_y(lat,lng):
    pair = []
    sinLat = math.sin((lat*math.pi)/180.0)

    x = ((lng+180.0)/360.0)
    y = (.5 - math.log((1.0 + sinLat)/(1.0 - sinLat)) / (4.0*math.pi))

    pair.append(x)
    pair.append(y)

    return pair

"""
Duplicating function: to be fixed later
"""
def lat_long_to_x_y_list(lng_lat):
    pair = []
    sinLat = math.sin((lng_lat[1]*math.pi)/180.0)

    x = ((lng_lat[0]+180.0)/360.0)
    y = (.5 - math.log((1.0 + sinLat)/(1.0 - sinLat)) / (4.0*math.pi))

    pair.append(x)
    pair.append(y)
    #print(lng_lat[1], lng_lat[0]);
    return pair

def dot_product(v1,v2):
    """
    Take the dot product of two vectors; v1 and v2 are arrays.
    """
    return v1[0] * v2[0] + v1[1] * v2[1]

def compute_distance(incident_x_y, segment_start, segment_end):
    deltaX_btwn_endpoints = segment_end[0] - segment_start[0]
    deltaY_btwn_endpoints = segment_end[1] - segment_start[1]

    segment_deltas = [deltaX_btwn_endpoints,deltaY_btwn_endpoints]

    deltaX_btwn_incident_and_segment_start = incident_x_y[0] - segment_start[0]
    deltaY_btwn_incident_and_segment_start = incident_x_y[1] - segment_start[1]

    incident_start_deltas = [deltaX_btwn_incident_and_segment_start, deltaY_btwn_incident_and_segment_start]

    """
    t is a parameter of the line segment. We compute the value of t, where the incident point orthogonally projects to the extended line segment.
    If t is less than 0, it projects before the startpoint. If t is greater than 1, it projects after the endpoint. Otherwise, it projects interior to
    the line segment.
    """
    t = dot_product(segment_deltas,incident_start_deltas)

    if t <= 0:
        #startpoint is closest to incident point
        return math.sqrt(dot_product(incident_start_deltas, incident_start_deltas))

    squared_length_of_segment_deltas = dot_product(segment_deltas,segment_deltas)

    if t >= squared_length_of_segment_deltas:
        #endpoint is closest to incident point

        """
        compute incident_end_deltas
        """
        deltaX_btwn_incident_and_segment_end = incident_x_y[0] - segment_end[0]
        deltaY_btwn_incident_and_segment_end = incident_x_y[1] - segment_end[1]

        incident_end_deltas = [deltaX_btwn_incident_and_segment_end,deltaY_btwn_incident_and_segment_end]

        return math.sqrt(dot_product(incident_end_deltas,incident_end_deltas))
    """
    The closest point is interior to segment.
    """
    interior_closest = dot_product(incident_start_deltas,incident_start_deltas) - ((t*t)/squared_length_of_segment_deltas)
    if interior_closest < 0:
        return 0
    else:
        return math.sqrt(interior_closest)

def ms_to_approx_hours(num_ms):
    return int(num_ms/(1000*60*60))
    
    
def process_data():
    service_requests = simplejson.load(urllib.urlopen(service_requests_url))
    centerlines = simplejson.load(urllib.urlopen(centerlines_url))

    service_requests_x_y = []

    for i in range(len(service_requests["rows"])):
        lat = float(service_requests["rows"][i]["value"][1]["lat"])
        lng = float(service_requests["rows"][i]["value"][1]["long"])
        if lat != 0.0 and lng != 0.0:
            service_requests_x_y.append(lat_long_to_x_y(lat,lng))

    line_segments = []

    for i in range(len(centerlines["features"])):
        sub_segments = centerlines["features"][i]["geometry"]["coordinates"]
        line_segments.append(sub_segments)
    
    line_segments_x_y = []
    for i in range(len(line_segments)):
        line_segments_x_y.append(map(lat_long_to_x_y_list, line_segments[i]))

    street_index = 0
    response_time_average = [0] * len(line_segments_x_y)
    response_time_sum = [0] * len(line_segments_x_y)
    street_count = [0] * len(line_segments_x_y)

    avg = 0
    response_time_totals = [0]*6
    
    for i in range(len(service_requests_x_y)):
        print i
        distance = 200;
        for j in range(len(line_segments_x_y)):
            for k in range(len(line_segments_x_y[j])-1):
                computed_distance = compute_distance(service_requests_x_y[i],line_segments_x_y[j][k],line_segments_x_y[j][k+1])
                if (distance > computed_distance):
                    distance = computed_distance
                    street_index = j
                
        street_count[street_index] = street_count[street_index] + 1
        response_time_sum[street_index] = response_time_sum[street_index] + int(service_requests["rows"][i]["value"][0])
        response_time_average[street_index] = response_time_sum[street_index]/street_count[street_index]

    for i in range(len(response_time_average)):
        avg = ms_to_approx_hours(response_time_average[i])
        if avg < 96:
            response_time_totals[0] = response_time_totals[0] + 1
        elif avg < 192:
            response_time_totals[1] = response_time_totals[1] + 1
        elif avg < 288:
            response_time_totals[2] = response_time_totals[2] + 1
        elif avg < 384:
            response_time_totals[3] = response_time_totals[3] + 1
        elif avg < 480:
            response_time_totals[4] = response_time_totals[4] + 1
        else:
            response_time_totals[5] = response_time_totals[5] + 1
    print response_time_totals

    sub_centerlines = {"type": "FeatureCollection","features":[]}

    for i in range(len(centerlines["features"])):
        centerlines["features"][i]["properties"]["response_time"] = ms_to_approx_hours(response_time_average[i])

        if(response_time_average[i] > 384):
            sub_centerlines["features"].append(centerlines["features"][i]);
    print len(sub_centerlines["features"])
    print response_time_totals        

    f = open('output/avg_response_times.geojson','w') 
    simplejson.dump(centerlines,f)
    f.close()
    f2 = open('output/avg_response_times_sub.json','w')
    simplejson.dump(sub_centerlines,f2)
    f2.close()
process_data()
