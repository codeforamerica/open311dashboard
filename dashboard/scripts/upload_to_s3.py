#Authors: Michael Lawrence Evans + Joanne Cheng
import os
import sys
import boto
from boto.s3.key import Key

#Use this if you want to use the create_bucket method
#from boto import s3

def percent_cb(complete, total):
  sys.stdout.write('.')
  sys.stdout.flush()

def upload_to_s3():
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
      print 'Uploading %s/%s to Amazon bucket %s' % (root, f, bucket_name) #debugging
      
      file_name = root + '/' + f
      
      k.key = file_name
      k.set_contents_from_filename(file_name,cb=percent_cb,num_cb=10)

upload_to_s3()