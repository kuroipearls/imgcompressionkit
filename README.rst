Image Compression (Halftoning & BTC)
----------

This package consists of 2 image compression techniques : **Halftoning** (binary 0 / 1) and **Block Truncation Coding - BTC** (max value / min value). 

*Package ini terdiri dari 2 teknik untuk melakukan kompresi gambar : Halftoning ~ biner 0 / 1 dan Block Truncation Coding - BTC ~ nilai maks / nilai min*. 

To install this package, you can use this command on your cmd / terminal. 

*Untuk melakukan instalasi package ini, gunakan command berikut pada cmd / terminal*.
::

	>>> pip install imagecompressionkit

This package can handle if you want to do halftoning / BTC on multiple images at once. You only need to put all of your images in the same folder. 

*Package ini bisa melakukan halftoning / BTC pada beberapa gambar secara otomatis. Hal yang perlu diperhatikan adalah, letakkan seluruh gambar yang ingin diproses pada satu folder yang sama*. 

**Note** : The first parameter is always your images dataset directory. 

*Catatan : parameter pertama akan selalu diisi oleh direktori dataset gambar anda*.

Halftoning : Error Diffusion (ED), Ordered Dithering (OD), Dot Diffusion(DD), Direct Binary Search(DBS) - Efficient Implementation. 

To use halftoning, you can type these lines on your codes.

*Untuk melakukan proses halftoning, gunakan sintaks berikut pada kodingan anda*.
::

	>>> import imgcompressionkit
	>>> imgcompressionkit.errorDiffusion('../datasets', 'floyd-steinberg', 127.5)
	>>> imgcompressionkit.orderedDithering('../datasets', 8)
	>>> imgcompressionkit.dotDiffusion('../datasets', 'knuth8', 127.5)
	>>> imgcompressionkit.edbs('../datasets', 'OD')

Block Truncation Coding : Basic BTC, Error Diffusion BTC (EDBTC), Ordered Dithering BTC (ODBTC), Dot Diffusion BTC (DDBTC). 

To use block truncation coding, you can use type these lines on your codes.

*Untuk melakukan proses block truncation coding, gunakan sintaks berikut pada kodingan anda*.
::

	>>> import imgcompressionkit
	>>> imgcompressionkit.btc('../datasets', 8)
	>>> imgcompressionkit.edbtc('../datasets', 'floyd-steinberg', 8)
	>>> imgcompressionkit.odbtc('../datasets', 8)
	>>> imgcompressionkit.ddbtc('../datasets', 'knuth8')

For further explanations & parameters on each method, this .README file will be updated further. Thanks.

*Untuk penjelasan lebih lanjut & penjelasan parameter pada setiap metode, file .README ini akan diperbarui lebih lanjut. Terima kasih*.