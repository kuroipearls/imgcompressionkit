import imgcompressionkit.tools as tools
import imgcompressionkit.algorithms as algorithms

import sys
import numpy as np

def errorDiffusion(dirName, ktype, threshold):
	# # # parameter needed : directory, kernel type, threshold.
	# # directory : your dataset directory.
	# # ktype : kernel type, only accept two kind of parameters: 'floyd-steinberg' or 'jajuni' (jarvis, judice, ninke)
	# # threshold : your selected threshold.

	print("Processing for error diffusion !")
	listImgs = tools.loadDirectory(dirName)
	outDir = 'results'
	tools.createDir(outDir)
	
	for(idx, imgname) in enumerate(listImgs):
		image = tools.readImage(imgname)
		height, width = tools.getInfo(image)
		source = np.copy(image)

		if ktype == 'floyd-steinberg':
			pad = 1
		elif ktype == 'jajuni':
			pad = 2
		else:
			print("Error ! Please choose your kernel type correctly ! Options available = floyd-steinberg and jajuni . ")
			sys.exit(1)

		image = algorithms.errorDif(image, height, width, ktype, threshold, pad)
		tools.saveImage(image, idx, "ED")
		print(tools.psnr(np.uint8(source), np.uint8(image)))

def orderedDithering(dirName, ksize):
	# # # parameter needed : directory, kernel type. 
	# # directory : your dataset directory.
	# # ktype : kernel type, only accept two kind of parameters: 'bayer8dispersed' or 'bayer8clustered'

	print("Processing for ordered dithering !")
	listImgs = tools.loadDirectory(dirName)
	outDir = 'results'
	tools.createDir(outDir)

	for(idx, imgname) in enumerate(listImgs):
		image = tools.readImage(imgname)
		height, width = tools.getInfo(image)
		source = np.copy(image)

		image = algorithms.orderedDith(image, height, width, ksize)
		tools.saveImage(image, idx, "OD")
		print(tools.psnr(np.uint8(source), np.uint8(image)))

def dotDiffusion(dirName, ktype, threshold):
	# # # parameter needed : directory, kernel (order) type, threshold. 
	# # directory : your dataset directory. 
	# # ktype : kernel order type. 
	# # threshold : your selected threshold. 

	print("Processing for dot diffusion !")
	listImgs = tools.loadDirectory(dirName)
	outDir = 'results'
	tools.createDir(outDir)

	for(idx, imgname) in enumerate(listImgs):
		image = tools.readImage(imgname)
		height, width = tools.getInfo(image)
		source = np.copy(image)

		image = algorithms.dotDiff(image, height, width, ktype, threshold)
		tools.saveImage(image, idx, "DD")
		print(tools.psnr(np.uint8(source), np.uint8(image)))

def edbs(dirName, prior):
	print("Processing for direct binary search !")
	listImgs = tools.loadDirectory(dirName)
	outDir = 'results'
	tools.createDir(outDir)

	for(idx, imgname) in enumerate(listImgs):
		image = tools.readImage(imgname)
		height, width = tools.getInfo(image)
		source = np.copy(image)

		if prior == 'ED':
			# the configs are fixed
			ktype = 'floyd-steinberg'
			threshold = 127.5
			pad = 1
			imageHT = algorithms.errorDif(image, height, width, ktype, threshold, pad)
		elif prior == 'OD':
			# the configs are fixed
			ksize = 8
			imageHT = algorithms.orderedDith(image, height, width, ksize)
		else:
			print('Error ! Please choose your prior halftoning method correctly ! Options available = ED and OD .')

		image = algorithms.edbSearch(image, imageHT, height, width)
		tools.saveImage(image, idx, "EDBS")
		print(tools.psnr(np.uint8(source), np.uint8(image)))

def btc(dirName, bs):
	print("Processing for block truncation coding !")
	listImgs = tools.loadDirectory(dirName)
	outDir = 'results'
	tools.createDir(outDir)

	for(idx, imgname) in enumerate(listImgs):
		image = tools.readImage(imgname)
		height, width = tools.getInfo(image)
		source = np.copy(image)

		image = algorithms.btcoding(image, height, width, bs)
		tools.saveImage(image, idx, "BTC")
		print(tools.psnr(np.uint8(source), np.uint8(image)))

def edbtc(dirName, ktype, bs):
	# # # parameter needed : directory, kernel type.
	# # directory : your dataset directory.
	# # ktype : kernel type, only accept two kind of parameters: 'floyd-steinberg' or 'jajuni' (jarvis, judice, ninke)

	print("Processing for error diffusion block truncation coding !")
	listImgs = tools.loadDirectory(dirName)
	outDir = 'results'
	tools.createDir(outDir)
	
	for(idx, imgname) in enumerate(listImgs):
		image = tools.readImage(imgname)
		height, width = tools.getInfo(image)
		source = np.copy(image)

		if ktype == 'floyd-steinberg':
			pad = 1
		elif ktype == 'jajuni':
			pad = 2
		else:
			print("Error ! Please choose your kernel type correctly ! Options available = floyd-steinberg and jajuni . ")
			sys.exit(1)

		image = algorithms.edbtcoding(image, height, width, ktype, pad, bs)
		tools.saveImage(image, idx, "EDBTC")
		print(tools.psnr(np.uint8(source), np.uint8(image)))

def odbtc(dirName, ksize):
	# # # parameter needed : directory, kernel type. 
	# # directory : your dataset directory.
	# # ktype : kernel type, only accept two kind of parameters: 'bayer8dispersed' or 'bayer8clustered'

	print("Processing for ordered dithering block truncation coding !")
	listImgs = tools.loadDirectory(dirName)
	outDir = 'results'
	tools.createDir(outDir)

	for(idx, imgname) in enumerate(listImgs):
		image = tools.readImage(imgname)
		height, width = tools.getInfo(image)
		source = np.copy(image)

		image = algorithms.odbtcoding(image, height, width, ksize)
		tools.saveImage(image, idx, "ODBTC")
		print(tools.psnr(np.uint8(source), np.uint8(image)))

def ddbtc(dirName, ktype):
	# # # parameter needed : directory, kernel (order) type, threshold. 
	# # directory : your dataset directory. 
	# # ktype : kernel order type. 

	print("Processing for dot diffusion block truncation coding !")
	listImgs = tools.loadDirectory(dirName)
	outDir = 'results'
	tools.createDir(outDir)

	for(idx, imgname) in enumerate(listImgs):
		image = tools.readImage(imgname)
		height, width = tools.getInfo(image)
		source = np.copy(image)

		image = algorithms.ddbtcoding(image, height, width, ktype)
		tools.saveImage(image, idx, "DDBTC")
		print(tools.psnr(np.uint8(source), np.uint8(image)))