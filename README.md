Mangareader to ebooks support epub and pdf format.

## Requirement

* python 2.7

## Credit

* mdl.py is base on [mdl.rb](https://github.com/lukaszkorecki/mdl)


## Download Images from mangareader.net

	$ruby mdl.py <START URL> <OUTPUT DIR> 

Example :

	$python mdl.py http://www.mangareader.net/bleach/482 Bleach

OR :

	$ruby mdl.py http://www.mangareader.net/bleach/482 ./

## Make epub

	$python makepub.py <dir> <image format>

Example :

	$python makepub.py Bleach_482 jpg

You will get epub file in output folder

## Make PDF

	$python makePDF.py <dir> <image format>
	
Example :

	$python makePDF.py Bleach_482 jpg
