#Bing Map Tile Downlaod

###Language: Python 3.6

###Input: Top Latitude, Top Longitude, Bottom Latitude, Bottom Longitude

###Output: Image bounded by Latitude Longitude rectangle

###Running instructions:

main.py downloads the relevant map tiles from Bing servers

$> python map.py <top_lat> <top_long> <bottom_lat> <bottom_long>

After all the tiles have been downloaded, run stichTiles.py to mergr files
and then crop it to fit the bounding rectangle

$> python stichTiles.py