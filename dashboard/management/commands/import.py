from osgeo import ogr
from django.contrib.gis.utils import LayerMapping

from dashboard.models import Street

ogr.UseExceptions()
shapefile = ''

source = ogr.Open(shapefile, 1)

city_id_def = ogr.FieldDefn('CITY_ID', ogr.OFTInteger)
layer = source.GetLayer()
layer.CreateField(city_id_def)

for feature in layer:
    feature.SetField('CITY_ID', 1)
    layer.SetFeature(feature)
    print "%s : %s" % (feature.GetField('STREETN_GC'), feature.GetField('CITY_ID'))


mapping = {'line': 'LINESTRING',
        'street_name': 'STREETN_GC',
        'left_low_address': 'LF_FADD',
        'left_high_address': 'LF_TOADD',
        'right_low_address': 'RT_FADD',
        'right_high_address': 'RT_TOADD',
        'city': {'id': 'CITY_ID'}}

lm = LayerMapping(Street, shapefile, mapping)
lm.save(verbose=True)
