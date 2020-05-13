from setuptools import setup

def readme():
	with open('README.rst') as f:
		return f.read()

setup(name='imgcompressionkit',
	version='0.3',
	description='Image compression kit for halftoning and block truncation coding (BTC).',
	long_description='Image compression kit for halftoning and block truncation coding (BTC).',
	keywords=['halftoning', 'block truncation coding', 'image compression'],
	url='https://github.com/kuroipearls/imgcompressionkit',
	author='kuroipearls',
	author_email='dellafitrayani@gmail.com',
	license='MIT',
	packages=['imgcompressionkit'],
	install_requires=[
		'numpy',
		'pillow',
		'opencv-python',
		'scipy',
	],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.7',
	],
	test_suite='nose.collector',
	tests_require=['nose', 'nose-cover3'],
	include_package_data=True,
	zip_safe=False)