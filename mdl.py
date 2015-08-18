import sys,urllib2,os,httplib,glob,shutil,json
from urllib import urlretrieve
from urlparse import urlparse
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

def getit(dirname,target_url,setting):

	print ">>> " + target_url
	try:
		req = urllib2.Request(target_url)
		response = urllib2.urlopen(req)
		the_page = response.read()

		soup = BeautifulSoup.BeautifulSoup(the_page)
	
		imgholder = soup.find(setting["image"]["parent"], attrs=setting["image"]["attr"]).find(setting["image"]["target"])
		next_url = setting["url"]
		url = soup.find(setting["next"]["parent"], attrs=setting["next"]["attr"]).find(setting["next"]["target"])

		if imgholder['href'] == 'javascript:void(0);':
			exit(0)

		href_parser = urlparse(imgholder['href'])
		count = len(href_parser.path.split('/')) # if href is relative path like 1.html
		if count == 1:
			target_url_parser = urlparse(target_url)
			segment = target_url_parser.path.split('/')
			segment[-1] = imgholder['href'] # replace last segment with next url
			next_url += "/".join(segment)
		elif count > 1 and href_parser.netloc == '' : # if href is relative path like /manga/01/1.html
			next_url += imgholder['href']
		else : # if href is absolute url
			next_url = imgholder['href']
		
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
		print ">>> Invalid url, Fail at "+target_url
		print ">>> Start cleaning"
		cleanup(dirname)

nexturl = sys.argv[1]

host = nexturl.split('/')
hostnameWithoutWWW = host[0] + "//" + host[2]
hostnameWithWWW = host[0] + "//www." + host[2]

setting = {}

json_data=open('setting.json')
data = json.load(json_data)

for x in data:
	if x["url"]  == hostnameWithoutWWW or x["url"]  == hostnameWithWWW:
		setting = x
		break

json_data.close()

if len(setting) == 0:
	print ">>> Site not found in setting file, Fail"
	exit
else:
	while nexturl:
		nexturl = getit(sys.argv[2],nexturl,setting)
