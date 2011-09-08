from sys import argv
import urllib
import json as simplejson
#2-D approximation
def compute_area_of_polygon(polygon_points):
  area = 0
  num_of_vertices = len(polygon_points)
  j = num_of_vertices - 1
  
  for i in xrange(num_of_vertices):
    point1 = polygon_points[i]
    point2 = polygon_points[j]
        
    area = area + point1[0]*point2[1]
    area = area - point1[1]*point2[0]
    
    j = i
  
  area = .5 * area
  
  return area

def compute_centroid(polygon_points):
  num_of_vertices = len(polygon_points)

  # do a line
  if (num_of_vertices == 2):
    x = (polygon_points[0][0] + polygon_points[1][0])/2
    y = (polygon_points[0][1] + polygon_points[1][1])/2

    return [x, y]


  j = num_of_vertices - 1
  x = 0
  y = 0
  
  for i in xrange(num_of_vertices):
    point1 = polygon_points[i]
    point2 = polygon_points[j]

    diff = point1[0]*point2[1] - point2[0]*point1[1]
    
    x = x + diff * (point1[0]+point2[0])
    y = y + diff * (point1[1]+point2[1])
    
    j = i
    
  factor = 6 * compute_area_of_polygon(polygon_points)
  
  centroid = [x/factor,y/factor]

  return centroid

if __name__ == '__main__':
  script,input_file = argv
  
  geojson_url = input_file
  geojson = simplejson.load(urllib.urlopen(geojson_url))
  
  for i in xrange(len(geojson['features'])):
    print i
    if len(geojson['features'][i]['geometry']['coordinates'][0]) > 1:
      polygon_points = geojson['features'][i]['geometry']['coordinates'][0]
    else:
      polygon_points = geojson['features'][i]['geometry']['coordinates'][0][0]

    compute_centroid(polygon_points)
  
  

