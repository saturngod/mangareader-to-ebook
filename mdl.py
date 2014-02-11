import sys,urllib2,os,httplib,glob,shutil,json
from urllib import urlretrieve
from module import BeautifulSoup
from pprint import pprint

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
		setting = {}
		req = urllib2.Request(target_url)
		response = urllib2.urlopen(req)
		the_page = response.read()

		host = target_url.split('/')
		hostnameWithoutWWW = host[0] + "//" + host[2]
		hostnameWithWWW = host[0] + "//" + host[2]

		soup = BeautifulSoup.BeautifulSoup(the_page)

		json_data=open('setting.json')
		data = json.load(json_data)
		for x in data:
			if x["url"]  == hostnameWithoutWWW or x["url"]  == hostnameWithWWW:
				setting = x
				break

		json_data.close()
		
		if len(setting) == 0:
			print ">>> Site not found in setting file, Fail"
			return False
	
		imgholder = soup.find(setting["image"]["parent"], attrs=setting["image"]["attr"]).find(setting["image"]["target"])
		next_url = setting["url"]
		url = soup.find(setting["next"]["parent"], attrs=setting["next"]["attr"]).find(setting["next"]["target"])

		if imgholder['href'].startswith("http") or imgholder['href'].startswith("www"):
			next_url = imgholder['href']
		else :
			next_url += imgholder['href']
		
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
while nexturl:
	nexturl = getit(sys.argv[2],nexturl)
