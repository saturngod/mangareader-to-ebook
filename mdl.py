import sys,urllib2,os,httplib,glob,shutil
from urllib import urlretrieve
from module import BeautifulSoup

def cleanup(dirname):
	for jpgFile in glob.glob(os.path.join(dirname, '*.jpg')):
		chapter_arr = jpgFile.split("-")
		chapter = chapter_arr[0]

		if not os.path.exists(chapter):
			os.makedirs(chapter)

		shutil.copy(jpgFile,chapter)
		os.remove(jpgFile)

	print ">>> Done"

def getit(dirname,target_url):

	print ">>> " + target_url
	try:
		req = urllib2.Request(target_url)
		response = urllib2.urlopen(req)
		the_page = response.read()

		soup = BeautifulSoup.BeautifulSoup(the_page)
		imgholder = soup.find("div", attrs={"id": "imgholder"}).find('a')
		next_url = "http://www.mangareader.net"
		next_url += imgholder['href'];

		url = soup.find("div", attrs={"id": "imgholder"}).find('img')
		url = url['src']

		lnk = url.split("/")
		name = lnk[-1]
		chapter = lnk[-2]
		
		if not os.path.exists(dirname):
			os.makedirs(dirname)

		if not os.path.exists(dirname+"/"+chapter+"-"+name):
			urlretrieve(url, dirname+"/"+chapter+"-"+name)

		return next_url

	except urllib2.URLError, e:
		print ">>> Fail at "+target_url
		print ">>> Start cleaning"
		cleanup(dirname)

	except httplib.InvalidURL , e:
		print ">>> Fail at "+target_url
		print ">>> Start cleaning"
		cleanup(dirname)

nexturl = sys.argv[1]
while nexturl:
	nexturl = getit(sys.argv[2],nexturl)
