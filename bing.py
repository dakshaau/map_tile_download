# http://ecn.t1.tiles.virtualearth.net/tiles/r012012012.png?g=685&mkt=en-us

#------------------------------------------------------------------------------
# <copyright company="Microsoft">
#     Copyright (c) 2006-2009 Microsoft Corporation.  All rights reserved.
# </copyright>
#------------------------------------------------------------------------------


import numpy as np

class TileSystem:
	EarthRadius = 6378137.
	MinLatitude = -85.05112878
	MaxLatitude = 85.05112878
	MinLongitude = -180
	MaxLongitude = 180

	# def __init__(self):
	# 	pass

	def Clip(self, n, minValue, maxValue):
		return min(max(n, minValue), maxValue)

	def MapSize(self, levelOfDetail):
		return 256 << levelOfDetail

	def GroundResolution(self, latitude, levelOfDetail):
		latitude = Clip(latitude, self.MinLatitude, self.MaxLatitude)
		return np.cos(latitude * np.pi / 180.) * 2 * np.pi * self.EarthRadius / MapSize(levelOfDetail)

	def MapScale(self, latitude, levelOfDetail, screenDpi):
		return GroundResolution(latitude, levelOfDetail) * screenDpi / 0.0254;

	def LatLongToPixelXY(self, latitude, longitude, levelOfDetail):
		latitude = Clip(latitude, self.MinLatitude, self.MaxLatitude);
		longitude = Clip(longitude, self.MinLongitude, self.MaxLongitude);

		x = (longitude + 180) / 360; 
		sinLatitude = np.sin(latitude * Math.PI / 180);
		y = 0.5 - np.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * np.pi);

		mapSize = MapSize(levelOfDetail);
		pixelX = Clip(x * mapSize + 0.5, 0, mapSize - 1);
		pixelY = Clip(y * mapSize + 0.5, 0, mapSize - 1);
		
		return pixelX, pixelY

	def PixelXYToLatLong(pixelX, pixelY, levelOfDetail):
		mapSize = MapSize(levelOfDetail)
		x = (Clip(pixelX, 0, mapSize-1) / mapSize) - 0.5
		y = 0.5 - (Clip(pixelY, 0, mapSize - 1) / mapSize)

		latitude = 90. - 360. * np.atan(np.exp(-y * 2 * np.pi)) / np.pi
		longitude = 360. * x

		return latitude, longitude

	def PixelXYToTileXY(pixelX, pixelY):
		return pixelX/256., pixelY/256.

	def TileXYToPixelXY(tileX, tileY):
		return tileX*256., tileY*256.

	def TileXYToQuadKey(tileX, tileY, levelOfDetail):
		quadKey = ''
		for i in range(levelOfDetail,-1,-1):
			digit = 0
			mask = 1 << (i-1)
			if (tileX & mask) != 0:
				digit += 1
			if (tileY & mask) != 0:
				digit += 1
				digit += 1
			quadKey += str(digit)
		return quadKey

	def QuadKeyToTileXY(quadKey):
		tileX = tileY = 0
		levelOfDetail = len(quadKey)
		for i in range(levelOfDetail,-1,-1):
			mask = 1 << (i-1)
			# if quadKey[levelOfDetail - i] == '0':
			# 	break
			if quadKey[levelOfDetail - i] == '1':
				tileX |= mask
			elif quadKey[levelOfDetail - i] == '2':
				tileY |= mask
			elif quadKey[levelOfDetail - i] == '3':
				tileX |= mask
				tileY |= mask
			elif quadKey[levelOfDetail - i] != '0':
				raise Exception('Invalid QuadKey digit sequence.')
