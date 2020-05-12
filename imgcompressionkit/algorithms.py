import imgcompressionkit.tools as tools

import numpy as np
import cv2

from scipy import signal
from scipy import misc
import math

def matError(ktype):
	if ktype == 'floyd-steinberg':
		err = np.array([7, 3, 5, 1], dtype=np.float32)
		errMapX = np.array([0, 1, 1, 1], dtype=np.uint8)
		errMapY = np.array([2, 0, 1, 2], dtype=np.uint8)
		err = np.float32(err / 16)
		return err, errMapX, errMapY
	else:
		err = np.array([7, 5, 3, 5, 7, 5, 3, 1, 3, 5, 3, 1], dtype=np.float32)
		errMapX = np.array([0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2], dtype=np.uint8)
		errMapY = np.array([3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4], dtype=np.uint8)
		err = np.float32(err / 48)
		return err, errMapX, errMapY

def errorDif(image, height, width, ktype, threshold, pad):
	image = np.pad(image, ((0,pad),(pad,pad)), 'constant', constant_values=0)
	kernel, kernelX, kernelY = matError(ktype)
	for i in range(0, height):
		for j in range(0, width):
			if image[i][j+1] > threshold:
				dummy = 255.0
			else:
				dummy = 0.0

			error = image[i][j+1] - dummy

			image[i][j+1] = dummy

			for value, valueX, valueY in zip(np.nditer(kernel), np.nditer(kernelX), np.nditer(kernelY)):
				image[i + valueX][j + valueY] = image[i + valueX][j + valueY] + error * value

	return np.uint8(image[0:height, 1:width+1])

def ditherArray(ktype):
	if ktype == 'bayer8dispersed':
		dArray = np.array([[0, 32, 8, 40, 2, 34, 10, 42],
			[48, 16, 56, 24, 50, 18, 58, 26],
			[12, 44, 4, 36, 14, 46, 6, 38],
			[60, 28, 52, 20, 62, 30, 54, 22],
			[3, 35, 11, 43, 1, 33, 9, 41],
			[51, 19, 59, 27, 49, 17, 57, 25],
			[15, 47, 7, 39, 13, 45, 5, 37],
			[63, 31, 55, 23, 61, 29, 53, 21]], dtype=np.float32)
	else:
		dArray = np.array([[62, 57, 48, 36, 37, 49, 58, 63],
			[56, 47, 35, 21, 22, 38, 50, 59],
			[46, 34, 20, 10, 11, 23, 39, 51],
			[33, 19, 9, 3, 0, 4, 12, 24],
			[32, 18, 8, 2, 1, 5, 13, 25],
			[45, 31, 17, 7, 6, 14, 26, 40],
			[55, 44, 30, 16, 15, 27, 41, 52],
			[61, 54, 43, 29, 28, 42, 53, 60]], dtype=np.float32)
	return tools.normalize(dArray)

def orderedDith(image, height, width, ktype):
	kernel = ditherArray(ktype)
	kheight, kwidth = tools.getInfo(kernel)
	bs = kheight
	loopHeight = np.uint8(height / bs)
	loopWidth = np.uint8(width / bs)

	image = tools.normalize(image)

	for i in range(0, loopHeight):
		for j in range(0, loopWidth):
			tempImg = image[i*bs:i*bs+bs,j*bs:j*bs+bs]

			for x in range(0, bs):
				for y in range(0, bs):
					if image[i*bs+x][j*bs+y] >= kernel[x][y]:
						image[i*bs+x][j*bs+y] = 255
					else:
						image[i*bs+x][j*bs+y] = 0
	return np.uint8(image)

def orderMat(ktype):
	# notes : the order Matrix has been reduced by 1 (x - 1) to help the calculation process.
	if ktype == 'knuth8':
		oMat = np.array([[34, 48, 40, 32, 29, 15, 23, 31],
			[42, 58, 56, 53, 21, 5, 7, 10],
			[50, 62, 61, 45, 13, 1, 2, 18],
			[38, 46, 54, 37, 25, 17, 9, 26],
			[28, 14, 22, 30, 35, 49, 41, 33],
			[20, 4, 6, 11, 43, 59, 57, 52],
			[12, 0, 3, 19, 51, 63, 60, 44],
			[24, 16, 8, 27, 39, 47, 55, 36]])
	return oMat

def matErrorDD():
	errDD = np.array([[1, 2, 1],
		[2, 0, 2],
		[1, 2, 1]], dtype=np.float32)
	errDD = np.float32(errDD / 16)
	return errDD

def dotDiff(image, height, width, ktype, threshold):
	ordKernel = orderMat(ktype)
	kheight, kwidth = tools.getInfo(ordKernel)

	# handle location for the order map
	patLoc = np.zeros((kheight * kwidth, 2))
	for m in range(0, kheight):
		for n in range(0, kwidth):
			patLoc[ordKernel[m][n]][0] = m
			patLoc[ordKernel[m][n]][1] = n
	patMaps = np.zeros((height, width))

	# get weight kernel (error kernel)
	weightKernel = matErrorDD()

	# create a dummy array to help calculation
	dumArray = np.copy(image)

	for i in range(0, height, kheight):
		for j in range(0, width, kwidth):
			index = 0
			while index != (kheight * kwidth):
				ni = int(i + patLoc[index][0])
				nj = int(j + patLoc[index][1])
				if dumArray[ni][nj] > threshold:
					dummy = 255
				else:
					dummy = 0
				error = dumArray[ni][nj] - dummy
				image[ni][nj] = dummy
				patMaps[ni][nj] = 1
				fm = 0
				for m in range(-1, 2):
					for n in range(-1, 2):
						if (ni + m >= 0) and (ni + m < height) and (nj + n >= 0) and (nj + n < width):
							if patMaps[ni + m][nj + n] == 0:
								fm = fm + weightKernel[m + 1][n + 1]

				for m in range(-1, 2):
					for n in range(-1, 2):
						if (ni + m >= 0) and (ni + m < height) and (nj + n >= 0) and (nj + n < width):
							if patMaps[ni + m][nj + n] == 0:
								dumArray[ni + m][nj + n] = dumArray[ni + m][nj + n] + (error * weightKernel[m + 1][n + 1] / fm)

				index = index + 1
	return np.uint8(image)

def edbSearch(image, imageHT, height, width):
	# normalize images
	image = tools.normalize(image)
	imageHT = tools.normalize(imageHT)

	gaussKernel = cv2.getGaussianKernel(7, -1)
	kernel = gaussKernel * np.transpose(gaussKernel)
	CPP = signal.convolve2d(kernel, kernel)

	err = imageHT - image
	CEP = signal.correlate2d(err, CPP)

	HalfCPPSize = 6
	HalfCPPSizeM = -6
	EPS = 0
	EPS_MIN = 0
	CountB = 1

	while CountB != 0:
		CountB = 0
		a0 = 0
		a1 = 0
		a0c = 0
		a1c = 0
		Cpx = 0
		Cpy = 0
		for i in range(0, height):
			for j in range(0, width):
				a0c = 0
				a1c = 0
				Cpx = 0
				Cpy = 0
				EPS_MIN = 0
				for y in range(-1, 2):
					if i + y < 0 or i + y > height - 1:
						continue
					for x in range(-1, 2):
						if j + x < 0 or j + x > width - 1:
							continue
						if y == 0 and x == 0:
							if imageHT[i][j] == 1:
								a0 = -1
								a1 = 0
							else:
								a0 = 1
								a1 = 0
						else:
							if imageHT[i+y][j+x] != imageHT[i][j]:
								if imageHT[i][j] == 1:
									a0 = -1
									a1 = -1 * a0
								else:
									a0 = 1
									a1 = -1 * a0
							else:
								a0 = 0
								a1 = 0
						EPS = (a0*a0+a1*a1)*CPP[HalfCPPSize][HalfCPPSize] + 2*a0*a1*CPP[HalfCPPSize+y][HalfCPPSize+x] + 2*a0*CEP[i+ HalfCPPSize][j+HalfCPPSize] + 2*a1*CEP[i+y+HalfCPPSize][j+x+HalfCPPSize]
						if EPS_MIN > EPS:
							EPS_MIN = EPS
							a0c = a0
							a1c = a1
							Cpx = x
							Cpy = y

				if EPS_MIN < 0:
					for y in range(HalfCPPSizeM, HalfCPPSize+1):
						for x in range(HalfCPPSizeM, HalfCPPSize+1):
							CEP[i+y+HalfCPPSize][j+x+HalfCPPSize] = CEP[i+y+HalfCPPSize][j+x+HalfCPPSize]+ a0c*CPP[y+HalfCPPSize][x+HalfCPPSize]

					for y in range(HalfCPPSizeM, HalfCPPSize+1):
						for x in range(HalfCPPSizeM, HalfCPPSize+1):
							CEP[i+y+Cpy+HalfCPPSize][j+x+Cpx+HalfCPPSize] = CEP[i+y+Cpy+HalfCPPSize][j+x+Cpx+HalfCPPSize]+a1c*CPP[y+HalfCPPSize][x+HalfCPPSize]

					imageHT[i][j] = imageHT[i][j] + a0c
					imageHT[Cpy+i][j+Cpx] = imageHT[i+Cpy][j+Cpx] + a1c
					CountB = CountB + 1

	return np.uint8(imageHT * 255)