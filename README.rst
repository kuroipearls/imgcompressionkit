Halftoning
----------

To use, you can do ::
	>>> import imgcompressionkit
	>>> imgcompressionkit.errorDiffusion('../datasets', 'floyd-steinberg', 127.5)
	>>> imgcompressionkit.orderedDithering('../datasets', 'bayer8clustered')
	>>> imgcompressionkit.dotDiffusion('../datasets', 'knuth8', 127.5)