import os,zipfile

#zipper function from http://coreygoldberg.blogspot.com/2009/07/python-zip-directories-recursively.html
def zipper(dir, zip_file):
	zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
	root_len = len(os.path.abspath(dir))
	for root, dirs, files in os.walk(dir):
		archive_root = os.path.abspath(root)[root_len:]
		for f in files:
			if (f!='.DS_Store'):
				fullpath = os.path.join(root, f)
				archive_name = os.path.join(archive_root, f)
				zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
	zip.close()
	return zip_file