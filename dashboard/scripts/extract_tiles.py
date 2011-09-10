import os
import sqlite3

def extract_tiles():
  """
  Shoutout to @rosskarchner: https://gist.github.com/837851
  Extracting images out of mbtiles. Creating folders and filenames.
  Need to add S3 support.
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

extract_tiles()
  
  