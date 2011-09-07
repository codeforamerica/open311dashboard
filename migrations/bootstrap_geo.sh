# Download and automagically migrate SF geographic data.
# @author Chris Barna <chris@unbrain.net>
DATABASE=open311

echo "Making temporary directory..."
mkdir tmp
cd tmp

for file in "realtor_neighborhoods" "StClines"
do
  echo "Downloading $file.zip..."
  curl -C - -O http://gispub02.sfgov.org/website/sfshare/catalog/$file.zip

  echo "Unzipping realtor_neighborhood.zip..."
  unzip $file.zip

  echo "Reprojecting and converting to GeoJSON"
  ogr2ogr -t_srs EPSG:4326 $file.4326.shp $file.shp
  ogr2ogr -f "GeoJSON" $file.4326.json $file.4326.shp

  echo "Cleaning up GeoJSON"
  cat $file.4326.json | grep "{ \"type\"" > $file.4326.clean.json

  if [ $file == 'realtor_neighborhoods' ]; then
    COLLECTION=polygons
    MIGRATION=../neighborhood_properties.js
  else
    COLLECTION=streets
    MIGRATION=../street_properties.js
  fi

  echo "Importing $COLLECTION into $DATABASE..."
  mongoimport -d $DATABASE -collection $COLLECTION -file $file.4326.clean.json

  echo "Running $MIGRATION"
  mongo $DATABASE $MIGRATION

  echo "Finished importing $COLLECTION"
done

echo "Cleaning up..."
cd ../
rm -rf tmp/
