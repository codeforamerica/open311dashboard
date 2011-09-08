# Download and automagically migrate SF geographic data.
# @author Chris Barna <chris@unbrain.net>
DATABASE=open311

echo "Making temporary directory..."
mkdir tmp
cd tmp
<<<<<<< HEAD
PWD=pwd
=======
>>>>>>> 6a90c4bfca54347b19113b8fd17f253658912ca5

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
<<<<<<< HEAD
    MIGRATION=mongoutils/migrations/polygons.py
  else
    COLLECTION=streets
    MIGRATION=mongoutils/migrations/streets.py
=======
    MIGRATION=../neighborhood_properties.js
  else
    COLLECTION=streets
    MIGRATION=../street_properties.js
>>>>>>> 6a90c4bfca54347b19113b8fd17f253658912ca5
  fi

  echo "Importing $COLLECTION into $DATABASE..."
  mongoimport -d $DATABASE -collection $COLLECTION -file $file.4326.clean.json

  echo "Running $MIGRATION"
<<<<<<< HEAD
  cd ../..
  python $MIGRATION
  cd migrations/tmp/
  # mongo $DATABASE $MIGRATION
=======
  mongo $DATABASE $MIGRATION
>>>>>>> 6a90c4bfca54347b19113b8fd17f253658912ca5

  echo "Finished importing $COLLECTION"
done

echo "Cleaning up..."
cd ../
rm -rf tmp/
