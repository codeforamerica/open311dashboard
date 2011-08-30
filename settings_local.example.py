# Django local settings
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# SECRET KEY
SECRET_KEY = ''

# Enagle Geographic data
ENABLE_GEO = True

# Open311 City
# See http://wiki.open311.org/GeoReport_v2/Servers
CITY = {
  'URL': 'https://open311.sfgov.org/dev/Open311/v2/requests.xml',
  'PAGINATE': True,
  'JURISDICTION': 'sfgov.org'
}
