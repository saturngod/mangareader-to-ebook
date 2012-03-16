import os,glob,sys,shutil,datetime

from module import zipfolder

if len(sys.argv) < 3:
	print "makeepub.py [folder] [image filetype]"

print "Create Tmp Dir..."
if not os.path.exists("./epubtmp"):
	os.makedirs("epubtmp")

path = sys.argv[1]
ext = sys.argv[2]
print "Reading Path : " + path

page_no = 1
for infile in glob.glob( os.path.join(path, '*.'+ext)):
    imgfile = str(page_no)+"."+ext
    shutil.copy(infile,"epubtmp/"+str(page_no)+"."+ext)
    img = """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html PUBLIC
	  "-//W3C//DTD XHTML 1.1//EN"
	  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type"
	  content="application/xhtml+xml; charset=utf-8" />
    <title></title>
    </head>
    <body style="padding:0px;margin:0px">"""
    img += "<img style=\"max-width:100%;max-height:100%\" src=\""+imgfile+"\"/>"
    img += """
      </body>
	</html>"""
    f = open("epubtmp/"+str(page_no)+".html",'w')
    f.write(img)
    f.close()
    page_no = page_no + 1

#create epub
if not os.path.exists("epubtmp/META-INF"):
	os.makedirs("epubtmp/META-INF")
xml = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
   <rootfiles>
      <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>"""
f = open("epubtmp/META-INF/container.xml","w")
f.write(xml)
f.close()

title = path
if(title[-1:]=="/"):
	title = title[:len(title)-1]

title = title.replace("/","-")

opf = """<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uuid_id">
  <metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:language>en</dc:language>
  <dc:identifier id="PrimaryID">urn:uuid:00000000-0000-0000-0000-000000000000</dc:identifier>
  <dc:creator>SGepub Convertor</dc:creator>
"""
opf +="<dc:title>"+title+"</dc:title>"
now = datetime.datetime.now()
opf +="<dc:date>"+now.strftime("%Y-%m-%dT%H:%M:%S+00:00")+"</dc:date>"
opf +="""</metadata>
  <manifest>
  <item id="ncx" href="content.ncx" media-type="application/x-dtbncx+xml"/>
  """

item = ""
itemref = ""

for k in range(1,page_no):
	item +="\n<item href=\""+str(k)+"."+ext+"\" id=\"added"+str(k)+"\" media-type=\""
	if(ext=="jpg"):
		item +="image/jpeg\"/>"
	elif(ext=="png"):
		item +="image/jpeg\"/>"
	else:
		item +="application/octet-stream\"/>"
	k = k + 1


for k in range(1,page_no):
	item +="\n<item href=\""+str(k)+".html\" id=\"html"+str(k)+"\" media-type=\"application/xhtml+xml\"/>"
	itemref +="\n<itemref idref=\"html"+str(k)+"\"/>"
	k = k+1

opf += item+ "\n</manifest>"
opf += "\n<spine toc=\"ncx\">"+itemref+"</spine>\n</package>"
f = open("epubtmp/content.opf","w")
f.write(opf)
f.close()

ncx = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"
ncx = """
<!DOCTYPE ncx PUBLIC
	  "-//NISO//DTD ncx 2005-1//EN"
	  "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">

<ncx version="2005-1"
     xml:lang="en"
     xmlns="http://www.daisy.org/z3986/2005/ncx/">

  <head>
    <meta name="dtb:uid" content="00000000-0000-0000-0000-000000000000"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>

  <docTitle><text>"""
ncx +=title
ncx +="""</text></docTitle>

  <docAuthor><text>SGepub Convertor</text></docAuthor>

  <navMap>
    <navPoint id="html1" playOrder="1">
      <navLabel><text>"""
ncx += title
ncx +="""</text></navLabel>
      <content src="1.html"/>
    </navPoint>
  </navMap>
</ncx>
"""

f = open("epubtmp/content.ncx","w")
f.write(ncx)
f.close()

f= open("epubtmp/mimetype","w")
f.write("application/epub+zip")
f.close()

#check output folder
if not os.path.exists("./output"):
	os.makedirs("output")

#zip it
zipfolder.zipper("./epubtmp","output/"+title+".epub")

print "Output file at output/"+title+".epub"

#remove Dir
shutil.rmtree("./epubtmp")