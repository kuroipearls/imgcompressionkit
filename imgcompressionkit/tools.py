import os
import glob
import PIL.Image
import numpy as np

def readImage(imgname):
	im = PIL.Image.open(imgname)
	return np.array(im.convert('L'), dtype=np.float32)

def loadDirectory(dirName):
	print("Loading image list from %s " % dirName) 
	images = sorted(glob.glob(os.path.join(dirName, '*.JPEG')))
	images += sorted(glob.glob(os.path.join(dirName, '*.jpg')))
	images += sorted(glob.glob(os.path.join(dirName, '*.png')))
	return images

def getInfo(image):
	return image.shape[0], image.shape[1]

def createDir(dirName):
	if not os.path.exists(dirName):
		os.makedirs(dirName)
		print("Directory ", dirName, " created !")
	else:
		print("Directory ", dirName, ' already exists !')

def saveImage(image, imgname, htType):
	out_directory = 'results'
	image = PIL.Image.fromarray(image.astype(np.uint8))
	# image.save('results/%s_%s.jpg' % (imgname, htType))
	image.save(os.path.join(out_directory, '%s_%s.jpg' % (imgname, htType)))

def mse(source, result):
	return np.square(np.subtract(source, result)).mean()

def psnr(source, result):
	return 10 * np.log10(255*255 / mse(source, result))

def normalize(image):
	return np.float32((image - image.min()) / (image.max() - image.min()) * 1)