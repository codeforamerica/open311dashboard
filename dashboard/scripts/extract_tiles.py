import os
import sqlite3

#for s3
import boto
import sys

from boto.s3.key import Key
"""
Shoutout to @rosskarchner: https://gist.github.com/837851
Extracting images out of mbtiles. Creating folders and filenames.
Need to add S3 support.
"""
def percent_cb(complete, total):
  sys.stdout.write('.')
  sys.stdout.flush()
  
def find_tiles(bucket_name,directory,file_type):
  #file_type is in format '.extension'
  """
  This function will find all the files of a certain file type within a directory.
  file_type is in format '.extension'
  
  >>> find_tiles('my_directory', '.png')
  """
  #walk the directory
  #find the pngs
  #once i find a png...upload_file(png_file)
  for root, dirs, files, in os.walk(directory):
    for file_name_file:
      if not file_name.endswith(file_type):
        #print root, file_name
        upload_file(root, file_name)
    #print dirs

def upload_file(bucket_name,root,png_file):
  #i would want to take its path name -- zoom/row/column.png
  #upload it to s3 with that pathname
  #then keep looking for more pngs
  bucket_name = 'open311'
  path_name =  '/'.join((bucket_name,root,file_name)) #tuple is more memory efficient than passing a list
  print path_name

def add_to_s3():
  aws_access_key_id = 'whatever it is'
  aws_secret_access_key = 'whatever it is'
  
  #assume that the bucket is already created??
  bucket_name = aws_access_key_id.lower() + '-name-of-bucket'
  conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
  
  bucket = conn.create_bucket(bucket_name, location=s3.connection.Location.DEFAULT)
  
  #Go through everything
  testfile ='filename'
  
  upload_file()
  
  
  print 'uploading %s to Amazon S3 bucket %s' % (testfile, bucket_name)
  
  k = Key(bucket)
  k.key = 'name of testfile' #?
  k.set_contents_from_filename(testfile, cb=percent_cb, num_cb=10)

def extract_tiles():
  #Connect to the database
  connection = sqlite3.connect('census_blocks.mbtiles')
  
  #Get everything out of the flat file
  pieces = conn.execute('select * from tiles').fetchall()
  
  for piece in pieces:
    #the image is a png
    zoom_level, row, column, image = piece
    
    try: 
      os.makedirs('%s/%s/' % (zoom_level,row))
    except:
      pass
    tile = open('%s/%s/%s.png' % (zoom_level, row, column), 'wb')
    tile.write(image)
    tile.close()
    
  #add_to_s3()
extract_tile()
  
  