# Bing Map Tile Downlaod

**Language:** Python 3.6

**Input:** Top Latitude, Top Longitude, Bottom Latitude, Bottom Longitude

**Output:** Image bounded by Latitude Longitude rectangle

### Running instructions:

main.py downloads the relevant map tiles from Bing servers. You need adminsitrator priviledges for this

**NOTE:** The maximum image resolution can be 20,512 X 20,512 pixels. If the maximum possible resolution
          for the complete image is greater than this, the code will discard the lat long pairs.

```Batchfile
python main.py <top_lat> <top_long> <bottom_lat> <bottom_long>
```

After all the tiles have been downloaded, run stitchTiles.py to merge files
and then crop it to fit the bounding rectangle

```Batchfile
python stitchTiles.py
```

Press `ESC` to close the display image and save cropped image.
