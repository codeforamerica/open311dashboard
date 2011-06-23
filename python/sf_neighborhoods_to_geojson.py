#!/usr/bin/python

import urllib
import json as simplejson
import pprint
import math

sf_polygons_url = 'input/sfPolygons.json'
metadata_url = 'input/service_requests_by_neighborhood_totals_final.json'

def process_data():
    sf_polygons = simplejson.load(urllib.urlopen(sf_polygons_url))
    metadata = simplejson.load(urllib.urlopen(metadata_url))

    for i in range(len(sf_polygons["polygons"])):
        for j in range(len(sf_polygons["polygons"][i]["Points"])):
            sf_polygons["polygons"][i]["Points"][j].reverse()

    total = 0

    metadata_counts = {metadata["rows"][0]["key"][0]:[[metadata["rows"][0]["key"][1],metadata["rows"][0]["value"]]]}
    
    for i in range(1,len(metadata["rows"])):
        total = total + metadata["rows"][i]["value"]
        
        if metadata["rows"][i]["key"][0] in metadata_counts:
            metadata_counts[metadata["rows"][i]["key"][0]].append([metadata["rows"][i]["key"][1],metadata["rows"][i]["value"]])
        else:
            metadata_counts[metadata["rows"][i]["key"][0]] = [[metadata["rows"][i]["key"][1] ,metadata["rows"][i]["value"]]]
        
    #sort
    #first sort alphabetically
    metadata_counts_first_sort = sorted(metadata_counts.items(),key=lambda neighborhoods: neighborhoods[0])
    
    #then sort by counts in each neighborhood
    metadata_counts_final = []
    for i in range(len(metadata_counts_first_sort)):
        interim_sort = sorted(metadata_counts_first_sort[i][1],key=lambda requests: requests[1])
        metadata_counts_final.append([metadata_counts_first_sort[i][0],interim_sort])
    geojson = {"type":"FeatureCollection","features":[]}

    k = 0
    totals = []

    for i in range(len(metadata_counts_final)):
        n_total = 0
        for j in range(len(metadata_counts_final[i][1])):
            n_total = n_total + metadata_counts_final[i][1][j][1]
        totals.append([i,n_total]);
    sorted_ranks = sorted(totals,key=lambda counts: counts[1])

    converted_sorted_ranks = [0] * len(sorted_ranks)

    for i in range(len(sorted_ranks)):
        converted_sorted_ranks[sorted_ranks[i][0]] = len(sorted_ranks)-i
    
    for i in range(len(sf_polygons["polygons"])):
            geojson["features"].append({"geometry":{"type":"LineString","coordinates":sf_polygons["polygons"][i]["Points"]},"type": "Feature","properties":{"neighborhood":sf_polygons["polygons"][i]["Name"],"top_five": metadata_counts_final[i][1][len(metadata_counts_final[i][1])-5:len(metadata_counts_final[i][1])],"total":totals[i][1],"rank":converted_sorted_ranks[i]}})
        
    print "ranks",converted_sorted_ranks
    f = open('output/sf_polygons_geojson_final.json','w')
    simplejson.dump(geojson,f)
    f.close()
process_data()
