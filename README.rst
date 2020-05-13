Image Compression (Halftoning & BTC)
----------

This package consists of 2 image compression techniques : Halftoning and Block Truncation Coding (BTC). 

Halftoning : Error Diffusion (ED), Ordered Dithering (OD), Dot Diffusion(DD), Direct Binary Search(DBS) - Efficient Implementation. 

To use halftoning, you can use ::

	>>> import imgcompressionkit
	>>> imgcompressionkit.errorDiffusion('../datasets', 'floyd-steinberg', 127.5)
	>>> imgcompressionkit.orderedDithering('../datasets', 16)
	>>> imgcompressionkit.dotDiffusion('../datasets', 'knuth8', 127.5)
	>>> imgcompressionkit.edbs('../datasets', 'OD')

Block Truncation Coding : Basic BTC, Error Diffusion BTC (EDBTC), Ordered Dithering BTC (ODBTC), Dot Diffusion BTC (DDBTC). 

To use block truncation coding, you can use ::

	>>> import imgcompressionkit
	>>> imgcompressionkit.btc('../datasets', 8)
	>>> imgcompressionkit.edbtc('../datasets', 'floyd-steinberg', 8)
	>>> imgcompressionkit.odbtc('../datasets', 8)
	>>> imgcompressionkit.ddbtc('../datasets', 'knuth8')