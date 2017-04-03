import cv2
import numpy as np
import os

if __name__ == '__main__':
	print('\nStitching together images ...')

	_, __, files = list(os.walk('Images'))[0]
	# print(len(files))
	files.sort(key = lambda x: (int(x.split(',')[0].split('_')[-1]), int(x.split(',')[1].split('.')[0])))
	# print(files[0])
	tilX = lambda x: int(x.split(',')[0].split('_')[-1])
	tilY = lambda x: int(x.split(',')[1].split('.')[0])
	Xs = sorted(list(set([tilX(x) for x in files])))
	Ys = sorted(list(set([tilY(x) for x in files])))
	fin_img = None
	vertical = None
	prev_x = None
	count = 0.
	tot = len(Xs)*len(Ys)
	prog = 0.
	for x in Xs:
		vertical = None
		for y in Ys:
			img = cv2.imread('Images/seq_{},{}.jpeg'.format(x,y))
			if vertical is None:
				vertical = img
			else:
				vertical = np.concatenate((vertical, img), axis=0)
			count+=1.
			prog = count/tot * 100
			print('\rCompleted: {:.2f}%'.format(prog),end=' ')
		if fin_img is None:
			fin_img = vertical
		else:
			fin_img = np.concatenate((fin_img, vertical), axis=1)
		
	print()
	print()
	cv2.imwrite('ArielView_org.jpeg',fin_img)
	h,w = fin_img.shape[:2]
	re_img = None
	if h <= w:
		ratio = float(h/w)
		re_img = cv2.resize(fin_img, (720 , int(ratio*720)))
	else:
		ratio = float(w/h)
		re_img = cv2.resize(fin_img, (int(ratio*720) , 720))
	while True:
		key = cv2.waitKey(10)
		if key == 27:
			break
		cv2.imshow('StitchedImage',re_img)
	# print(tilePixelXY[0][0],-tilePixelXY[2][0], tilePixelXY[0][1], -tilePixelXY[1][1])
	f = open('params.dat','r')
	params = f.readlines()[0]
	params.strip()
	tc, bc, tr, br = [int(x) for x in params.split(' ')]
	fin_img = fin_img[tr:-br, tc:-bc, :]
	cv2.imwrite('ArielView.jpeg',fin_img)
	print('Saved image at: {}'.format(os.path.abspath('ArielView.jpeg')))