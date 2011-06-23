#!/usr/bin/python

"""
311 + Centerlines
using floats everywhere?
"""
import urllib
import json as simplejson

import pprint

import math

import colorsys

service_requests_url = 'input/service_requests_density.json'
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

"""
Optimizations
TODO: Coarse Grid
Precompute everything for a given segment, save time by computing information about a segment once, instead of everytime you use a segment
Can take out square roots
"""
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
        #return dot_product(incident_start_deltas, incident_start_deltas)

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
        #return dot_product(incident_end_deltas,incident_end_deltas)
    """
    closest point is interior to segment
    """
    interior_closest = dot_product(incident_start_deltas,incident_start_deltas) - ((t*t)/squared_length_of_segment_deltas)
    if interior_closest < 0:
        return 0
    else:
        return math.sqrt(interior_closest)
    #return dot_product(incident_start_deltas,incident_start_deltas) - ((t*t)/squared_length_of_segment_deltas)
    
    
def process_data():
    service_requests = simplejson.load(urllib.urlopen(service_requests_url))
    centerlines = simplejson.load(urllib.urlopen(centerlines_url))
    print(len(centerlines["features"]))

    service_requests_x_y = []
    month_list = []
    request_list = []

    for i in range(len(service_requests["rows"])):
        lat = float(service_requests["rows"][i]["value"]["lat"])
        lng = float(service_requests["rows"][i]["value"]["long"])

        if lat != 0.0 and lng != 0.0:
            service_requests_x_y.append(lat_long_to_x_y(lat,lng))
            month_list.append(int(service_requests["rows"][i]["value"]["date"][5:7])) #maps to each request
            request_list.append(service_requests["rows"][i]["value"]["request_type"]) #maps to each request

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

    months_by_street_count = [[0]*12 for i in range(len(line_segments_x_y))]

    requests_by_street = [[] for i in range(len(line_segments_x_y))]

    for i in range(len(service_requests_x_y)):
        print i
        distance = 200;
        for j in range(len(line_segments_x_y)):
            for k in range(len(line_segments_x_y[j])-1):
                computed_distance = compute_distance(service_requests_x_y[i],line_segments_x_y[j][k],line_segments_x_y[j][k+1])
                if (distance > computed_distance):
                    distance = computed_distance
                    street_index = j

        months_by_street_count[street_index][month_list[i]-1] = months_by_street_count[street_index][month_list[i]-1] + 1

        requests_by_street[street_index].append(request_list[i])
        
        street_count[street_index] = street_count[street_index] + 1
    
    #max_count_list = [[]]*len(requests_by_street)
    max_count_list = []
    
    maximum = 0

    individual_counts = []
    
    for i in range(len(requests_by_street)):
        if len(requests_by_street[i]) > 0:
            #countlist = [0]*len(requests_by_street[i])
            individual_counts = [] #reset
        #print len(requests_by_street[i])
            for j in range(len(requests_by_street[i])):
                #print requests_by_street[i]
                individual_counts.append([requests_by_street[i].count(requests_by_street[i][j]),requests_by_street[i][j]])
                max_count = max(individual_counts)
            max_count_list.append(max_count)
        else:
            max_count_list.append([0,'None'])
        
        #print maximum
    print(max_count_list)
        #max_count_list.append(max(countlist))
    
    maximum = max(street_count)
    normalized_street_scores = map(lambda x: 100*math.log((1024/maximum)*x,2) if x > 0 else x,street_count)
    sub_centerlines = {"type": "FeatureCollection","features":[]}
    for i in range(len(centerlines["features"])):
        #centerlines["features"][i]["properties"]["score"] = street_count[i]
        centerlines["features"][i]["properties"]["score"] = normalized_street_scores[i]
        centerlines["features"][i]["properties"]["months"] = months_by_street_count[i]
        centerlines["features"][i]["properties"]["top_request_type"] = max_count_list[i]

        if(normalized_street_scores[i] > 500):
            sub_centerlines["features"].append(centerlines["features"][i]);
    print "sub_centerlines length: ",len(sub_centerlines["features"])
        

    f = open('output/scored_centerlines_sub_final.json','w')
    simplejson.dump(sub_centerlines,f)
    f.close()
    f2 = open('output/scored_centerlines_final.json','w')
    simplejson.dump(centerlines,f2)
    f2.close()
process_data()
