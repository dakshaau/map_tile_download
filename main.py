from bing import TileSystem
import requests
import cv2
import numpy as np

if __name__ == '__main__':
	t = TileSystem()
	print(t.EarthRadius)
	emptyImage = cv2.imread('Error.jpeg',0)

	## http://a0.ortho.tiles.virtualearth.net/tiles/a120200223.jpeg?g=2
	qKey = '1202002230022122121212'
	detail = len(qKey)
	tx, ty = t.QuadKeyToTileXY(qKey)
	px, py = t.TileXYToPixelXY(tx, ty)
	lat, lng = t.PixelXYToLatLong(px, py, detail)
	empty = 0
	while empty == 0:
		fileName = 'abc'
		file = open('Images/{}.jpeg'.format(fileName),'wb')
		response = requests.get('http://a0.ortho.tiles.virtualearth.net/tiles/a{}.jpeg?g=2'.format(qKey), stream=True)

		if not response.ok:
			# Something went wrong
			print('Invalid depth')

		for block in response.iter_content(1024):
			file.write(block)
		file.close()
		curimage = cv2.imread('Images/{}.jpeg'.format(fileName),0)
		empty = np.where(np.not_equal(curimage, emptyImage))[0].shape[0]
		if empty == 0:
			detail -= 1
			px, py = t.LatLongToPixelXY(lat, lng, detail)
			tx, ty = t.PixelXYToTileXY(px, py)
			qKey = t.TileXYToQuadKey(tx, ty, detail)
			print('Moving on, new QuadKey : {}'.format(qKey))