def create_bounding_box(points):
  #initialize
  lon_init = points[0][0]
  lat_init = points[0][1]

  minLon = lon_init
  maxLon = lon_init
  minLat = lat_init
  maxLat = lat_init

  for i in xrange(1,len(points)):
    if minLon > points[i][0]:
      minLon = points[i][0]
    if maxLon < points[i][0]:
      maxLon = points[i][0]
    if minLat > points[i][1]:
      minLat = points[i][1]
    if maxLat < points[i][1]:
      maxLat = points[i][1]

  bounding_box = [{'lat':minLat,'lon':minLon},{'lat':maxLat,'lon':maxLon}]
  return bounding_box

if __name__ == 'main':
  #Create array of test points
  points = [{'lat': 37.77017,'lon':-122.41996},{'lat': 37.77559,'lon':-122.41516},{'lat':37.77858,'lon':-122.42614}]
  create_bounding_box(points)
