# NOTE: The database name will more than likely be specific to your machine.
MONGODB = {
    'db' : 'open311',
    'host' : 'localhost',
}

# Open311 City
# See http://wiki.open311.org/GeoReport_v2/Servers
CITY = {
  'URL': 'https://open311.sfgov.org/dev/Open311/v2/requests.xml',
  'PAGINATE': True,
  'JURISDICTION': 'sfgov.org'
}
