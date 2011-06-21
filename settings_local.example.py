# Django local settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# SECRET KEY
SECRET_KEY = ''

# CITY Variable
CITY = {
        'NAME': '',         # Ex: 'San Francisco'
        'SHORTNAME': '',    # Ex: 'sf'
        'JURISDICTION': '', # From the city's API
        'URL': r'',         # GET requests URL
        'PAGINATE': False,  # Some implementations paginate, BOS does, SF doesn't.
        }
