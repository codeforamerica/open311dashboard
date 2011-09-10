import os
import sqlite3

import boto
import sys
from boto.s3.key import Key

#Use this if you want to use the create_bucket method
#from boto import s3

def percent_cb(complete, total):
  sys.stdout.write('.')
  sys.stdout.flush()

def extract_tiles():
  """
  Shoutout to @rosskarchner: https://gist.github.com/837851
  Extracting images out of mbtiles. Creating folders and filenames.
  """

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
  
  if to_upload:
    upload_to_s3()

def upload_to_s3():
  """
  Assists you in uploading a set of directories/files to S3. Assumes that your S3 bucket
  has already been created. Use the boto's create_bucket method if you don't have an existing bucket.
  """
  AWS_ACCESS_KEY_ID = 'Your AWS Access Key ID'
  AWS_SECRET_ACCESS_KEY = 'Your AWS Secret Access Key'
  
  #This is for making an extremely unique bucket name.
  #bucket_name = AWS_ACCESS_KEY_ID.lower() + 'Your desired bucket name'
  
  bucket_name = 'Your existing bucket name'
  
  #We connect!
  conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
  
  #Use this if you want to create a bucket
  #bucket = conn.create_bucket(bucket_name,location=s3.connection.Location.DEFAULT)
  
  #Connect to our existing bucket
  bucket = conn.get_bucket(bucket_name)
  
  #the base directory
  directory = 'base-directory'
  
  k = Key(bucket)
  
  for root, dirs, files in os.walk(directory):
    for f in files:
      print 'Uploading %s/%s to Amazon bucket %s' % (root, f, bucket_name)
      
      file_name = root + '/' + f
      
      k.key = file_name
      k.set_contents_from_filename(file_name,cb=percent_cb,num_cb=10)

if __name__ == '__main__':
  """
    Pass is in Boolean variable on the command line to specify whether you want to upload your tiles to Amazon S3.
    to_upload is a Boolean variable.
  """
  script,to_upload = argv
  extract_tiles()
  
