from bing import TileSystem
import requests
import cv2
import numpy as np
import sys
import os
import time

if __name__ == '__main__':
	arg = sys.argv[:]
	if len(arg) < 5:
		print('Not enough arguments!\n')
		print('python maine.py <top_lat> <top_long> <bot_lat> <bot_long>')
		exit(0)
	lt_lat = float(arg[1])
	lt_lng = float(arg[2])
	rb_lat = float(arg[3])
	rb_lng = float(arg[4])
	'''
	For the lat long coordinated to be positined as Top Left and Bottom Right
	the topleft_lat > bottomright_lat and topleft_long < bottomright_long
	
	If the above condition doesn't hold then the coodinated need to be swaped
	accordingly
	'''
	if lt_lat > rb_lat and lt_lng > rb_lng:
		temp = lt_lng
		lt_lng = rb_lng
		rb_lng = temp
	if lt_lat < rb_lat and lt_lng < rb_lng:
		temp = lt_lat
		lt_lat = rb_lat
		rb_lat = temp
	elif lt_lat < rb_lat and lt_lng > rb_lng:
		temp = lt_lng
		lt_lng = rb_lng
		rb_lng = temp
		temp = lt_lat
		lt_lat = rb_lat
		rb_lat = temp

	lb_lat = lt_lat
	lb_lng = rb_lng
	rt_lat = rb_lat
	rt_lng = lt_lng
	bnd_sqr = [(lt_lat, lt_lng), (rt_lat, rt_lng), (lb_lat, lb_lng), (rb_lat, rb_lng)]
	t = TileSystem()
	# print(t.EarthRadius)
	emptyImage = cv2.imread('Error.jpeg',0)

	## http://a0.ortho.tiles.virtualearth.net/tiles/a120200223.jpeg?g=2
	# qKey = '1202002230022122121212'
	levels = []
	keys = []
	# l_v = np.arange(lt_lng, lb_lng, 0.00001).tolist()
	# l_v = [(lt_lat, l) for l in l_v]
	# prevkey = ''
	'''
	Downloading the maximum levelOfDetail Map Tile available for the four corners of the bounding
	rectangle.

	'''
	if not os.path.exists('Images'):
		os.mkdir('Images')

	_, __, files = list(os.walk('Images'))[0]
	for file in files:
		os.remove(os.path.join(_,file))

	for i, (lat, lng) in enumerate(bnd_sqr):
		detail = 23
		# tx, ty = t.QuadKeyToTileXY(qKey)
		# px, py = t.TileXYToPixelXY(tx, ty)
		# lat, lng = t.PixelXYToLatLong(px, py, detail)
		px, py = t.LatLongToPixelXY(lat, lng, detail)
		tx, ty = t.PixelXYToTileXY(px, py)
		qKey = t.TileXYToQuadKey(tx, ty, detail)
		empty = 0
		while empty == 0:
			fileName = str(i)
			file = open('Images/seq_{}.jpeg'.format(fileName),'wb')
			response = requests.get('http://a0.ortho.tiles.virtualearth.net/tiles/a{}.jpeg?g=2'.format(qKey), stream=True)

			if not response.ok:
				# Something went wrong
				print('Invalid depth')

			for block in response.iter_content(1024):
				file.write(block)
			file.close()
			curimage = cv2.imread('Images/seq_{}.jpeg'.format(fileName),0)
			# while True:
			# 	key = cv2.waitKey(10)
			# 	if key == 27:
			# 		break
			# 	cv2.imshow('disp',curimage - emptyImage)
			empty = np.where(np.not_equal(curimage, emptyImage))[0].shape[0]
			# print(empty)
			if empty == 0:
				detail -= 1
				px, py = t.LatLongToPixelXY(lat, lng, detail)
				tx, ty = t.PixelXYToTileXY(px, py)
				qKey = t.TileXYToQuadKey(tx, ty, detail)
				# print('Moving on, new QuadKey : {}'.format(qKey))
		levels.append(detail)
		keys.append(qKey)
	min_level = min(levels)
	pixelXY = []

	[os.remove('Images/seq_{}.jpeg'.format(i)) for i in range(4)]
	# keys = []
	# print(levels)
	print('Selected levelOfDetail: {}'.format(min_level))
	'''
	Finding out the maximum common levelOfDetail for the tiles and redownloading accordingly.

	'''
	tileXY = []
	tilePixelXY = []
	for i, (level, (lat, lng)) in enumerate(zip(levels, bnd_sqr)):
		# print(level)
		# if level > min_level:
			# print('Blah')
			# lat, lng = coors
		px, py = t.LatLongToPixelXY(lat, lng, min_level)
		pixelXY.append((px, py))
		tx, ty = t.PixelXYToTileXY(px, py)
		tileXY.append((tx, ty))
		tpx, tpy = t.PixelXYToTilePixelXY(px, py)
		tilePixelXY.append((tpx, tpy))
		qKey = t.TileXYToQuadKey(tx, ty, min_level)
		fileName = '{},{}'.format(tx,ty)
		file = open('Images/seq_{}.jpeg'.format(fileName),'wb')
		response = requests.get('http://a0.ortho.tiles.virtualearth.net/tiles/a{}.jpeg?g=2'.format(qKey), stream=True)

		if not response.ok:
			# Something went wrong
			print('Invalid depth')

		for block in response.iter_content(1024):
			file.write(block)
		file.close()
		# keys.append(qKey)
		keys[i] = qKey
	# print(keys)
	# print(pixelXY)
	# print(tilePixelXY)
	print('Downlaoded corner tiles.')

	'''
	Calculating the pixelXY for lat long with
	'''
	tb = pixelXY[2][0] - pixelXY[0][0] + 1
	lr = pixelXY[1][1] - pixelXY[0][1] + 1
	# print(tb, lr)

	# print(tilePixelXY[0], tilePixelXY[2])
	# print(tilePixelXY[1], tilePixelXY[3])
	tileD_tb = (256-tilePixelXY[0][0]) + tilePixelXY[2][0] + 1
	tileD_lr = (256-tilePixelXY[0][1]) + tilePixelXY[1][1] + 1

	if (tileXY[1][1] - tileXY[0][1]) > 1 and (tileXY[2][0] - tileXY[0][0]) > 1:
		tb -= tileD_tb
		lr -= tileD_lr
	elif (tileXY[1][1] - tileXY[0][1]) > 1:
		lr -= tileD_lr
		tb = 0
	elif (tileXY[2][0] - tileXY[0][0]) > 1:
		tb -= tileD_tb
		lr = 0
	else:
		tb = 0
		lr = 0

	# print(tb/256, lr/256)
	if tb > 20000 or lr > 20000:
		print(int(tb/256), int(lr/256))
		print('Too many tiles. Reduce the bounding rectangle area!')
		exit(0)

	num_tiles_lr = int(lr/256)
	num_tiles_tb = int(tb/256)


	if num_tiles_tb > 0 and num_tiles_lr > 0:
		prog = 0.
		tot = (num_tiles_lr+2)*(num_tiles_tb+2)
		count = 0.
		print('Downloading remaining tiles, {} ...'.format(tot))
		for i in range(0,num_tiles_tb+2):
			tx = tileXY[0][0] + i
			for j in range(0,num_tiles_lr+2):
				ty = tileXY[0][1] + j
				qKey = t.TileXYToQuadKey(tx, ty, min_level)
				fileName = '{},{}'.format(tx,ty)
				file = open('Images/seq_{}.jpeg'.format(fileName),'wb')
				response = requests.get('http://a0.ortho.tiles.virtualearth.net/tiles/a{}.jpeg?g=2'.format(qKey), stream=True)

				if not response.ok:
					# Something went wrong
					print('Invalid depth')

				for block in response.iter_content(1024):
					file.write(block)
				count += 1.
				prog = (count/tot) * 100
				print('\rCompleted: {:.2f}%'.format(prog),end=' ')
		print()

	elif num_tiles_tb > 0:
		prog = 0.
		tot = num_tiles_tb
		count = 0.
		print('Downloading remaining tiles, {} ...'.format(tot))
		for i in range(1,num_tiles_tb+1):
			tx = tileXY[0][0] + i
			ty = tileXY[0][1]
			qKey = t.TileXYToQuadKey(tx, ty, min_level)
			fileName = '{},{}'.format(tx,ty)
			file = open('Images/seq_{}.jpeg'.format(fileName),'wb')
			response = requests.get('http://a0.ortho.tiles.virtualearth.net/tiles/a{}.jpeg?g=2'.format(qKey), stream=True)

			if not response.ok:
				# Something went wrong
				print('Invalid depth')

			for block in response.iter_content(1024):
				file.write(block)
			count += 1.
			prog = (count/tot) * 100
			print('\rCompleted: {:.2f}%'.format(prog),end=' ')
		print()

	elif num_tiles_lr > 0:
		prog = 0.
		tot = num_tiles_lr
		count = 0.
		print('Downloading remaining tiles, {} ...'.format(tot))
		for i in range(1,num_tiles_lr+1):
			tx = tileXY[0][0]
			ty = tileXY[0][1] + i
			qKey = t.TileXYToQuadKey(tx, ty, min_level)
			fileName = '{},{}'.format(tx,ty)
			file = open('Images/seq_{}.jpeg'.format(fileName),'wb')
			response = requests.get('http://a0.ortho.tiles.virtualearth.net/tiles/a{}.jpeg?g=2'.format(qKey), stream=True)

			if not response.ok:
				# Something went wrong
				print('Invalid depth')

			for block in response.iter_content(1024):
				file.write(block)
			file.close()
			count += 1.
			prog = (count/tot) * 100
			print('\rCompleted: {:.2f}%'.format(prog),end=' ')
		print()

	file = open('params.dat','w')
	file.write('{} {} {} {}'.format(tilePixelXY[0][0], 256-tilePixelXY[2][0], tilePixelXY[0][1], 256-tilePixelXY[1][1]))
	file.close()
	# time.sleep(6)

	# print('\nStitching together images ...')

	# _, __, files = list(os.walk('Images'))[0]
	# # print(len(files))
	# files.sort(key = lambda x: (int(x.split(',')[0].split('_')[-1]), int(x.split(',')[1].split('.')[0])))
	# # print(files[0])
	# tilX = lambda x: int(x.split(',')[0].split('_')[-1])
	# tilY = lambda x: int(x.split(',')[1].split('.')[0])
	# Xs = sorted(list(set([tilX(x) for x in files])))
	# Ys = sorted(list(set([tilY(x) for x in files])))
	# fin_img = None
	# vertical = None
	# prev_x = None
	# count = 0.
	# tot = len(Xs)*len(Ys)
	# prog = 0.
	# for x in Xs:
	# 	vertical = None
	# 	for y in Ys:
	# 		img = cv2.imread('Images/seq_{},{}.jpeg'.format(x,y))
	# 		if vertical is None:
	# 			vertical = img
	# 		else:
	# 			vertical = np.concatenate((vertical, img), axis=0)
	# 		count+=1.
	# 		prog = count/tot * 100
	# 		print('\rCompleted: {:.2f}%'.format(prog),end=' ')
	# 	if fin_img is None:
	# 		fin_img = vertical
	# 	else:
	# 		fin_img = np.concatenate((fin_img, vertical), axis=1)
		
	# print()
	# print()
	# cv2.imwrite('ArielView_org.jpeg',fin_img)
	# h,w = fin_img.shape[:2]
	# re_img = None
	# ratio = float(h/w)
	# re_img = cv2.resize(fin_img, (720 , int(ratio*720)))
	# while True:
	# 	key = cv2.waitKey(10)
	# 	if key == 27:
	# 		break
	# 	cv2.imshow('StitchedImage',re_img)
	# # print(tilePixelXY[0][0],-tilePixelXY[2][0], tilePixelXY[0][1], -tilePixelXY[1][1])
	# fin_img = fin_img[tilePixelXY[0][0]:-tilePixelXY[2][0], tilePixelXY[0][1]:-tilePixelXY[1][1], :]
	# cv2.imwrite('ArielView.jpeg',fin_img)
	# print('Saved image at: {}'.format(os.path.abspath('ArielView.jpeg')))
