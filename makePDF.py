from reportlab.lib.pagesizes import A2
from reportlab.platypus import SimpleDocTemplate, Image
import os,glob,sys,shutil

if len(sys.argv) < 3:
    print "makePDF.py [folder] [image filetype]"

if not os.path.exists("./PDF"):
    os.makedirs("PDF")

path = sys.argv[1]
ext = sys.argv[2]
print "Reading Path : " + path

#PDF Prepare

parts = []

title = path
if(title[-1:]=="/"):
    title = title[:len(title)-1]

title = title.replace("/","-")

doc = SimpleDocTemplate("./PDF/"+title+".pdf", pagesize=A2)

for infile in glob.glob( os.path.join(path, '*.'+ext)):
    parts.append(Image(infile))
print "Start Making PDF ...."
print "..."
doc.build(parts)
print "Outputt File at PDF/" + title +".pdf"