## Requirement

* ruby
* mechanize gem

* python 2.7

## Credit

* [mdl.rb](https://github.com/lukaszkorecki/mdl)


## Download Images from mangareader.net

	$ruby mdl.rb <OUTPUT DIR> <START URL>

Example :

	$ruby mdl.rb Bleach http://www.mangareader.net/bleach/482

OR :

	$ruby mdl.rb ./ http://www.mangareader.net/bleach/482

## Make epub

	$python makepub.py <dir> <image format>

Example :

	$python makepub.py Bleach_482/ jpg

You will get epub file in output folder