import os
import sqlite3

mbtiles_filename = 'filename.mbtiles'

def extract_tiles():
  """
  Shoutout to @rosskarchner: https://gist.github.com/837851
  Extracting images out of mbtiles. Creating folders and filenames.
  """

  #Connect to the database
  connection = sqlite3.connect(mbtiles_filename)
  
  #Get everything out of the flat file
  pieces = connection.execute('select * from tiles').fetchall()
  
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
  
  
