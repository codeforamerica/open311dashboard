def create_bounding_box(points):
  #initialize
  lon_init = points[0]['lon']
  lat_init = points[0]['lat']
  
  minLon = lon_init
  maxLon = lon_init
  minLat = lat_init
  maxLat = lat_init
  
  for i in xrange(1,len(points)):
    if minLon > points[i]['lon']:
      minLon = points[i]['lon']
    if maxLon < points[i]['lon']:
      maxLon = points[i]['lon']
    if minLat > points[i]['lat']:
      minLat = points[i]['lat']
    if maxLat < points[i]['lat']:
      maxLat = points[i]['lat']
  
  bounding_box = [{'lat':minLat,'lon':minLon},{'lat':maxLat,'lon':maxLon}]
  print bounding_box
  return bounding_box

if __name__ == 'main':
  #Create array of test points
  points = [{'lat': 37.77017,'lon':-122.41996},{'lat': 37.77559,'lon':-122.41516},{'lat':37.77858,'lon':-122.42614}]
  create_bounding_box(points)