#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import glob
import datetime
import argparse
from xml.dom.minidom import parse
from module import zipfolder


# process args
parser = argparse.ArgumentParser()
parser.add_argument('folder', nargs='*')
parser.add_argument('--ext', help="image filetype extension (jpg, png, ...). Default: jpg")
parser.add_argument('--resize', type=int, nargs=2, help="resize images according to width and height. Example: --resize 600 800")
options = parser.parse_args()

if len(sys.argv) < 2:
    print parser.print_help()
    sys.exit()

paths = options.folder

if options.ext:
    ext = options.ext
else:
    ext = "jpg"

if options.resize:
    try:
        import Image
    except ImportError:
        print "Python Image Library not installed. Install it with your package manager or download it at http://effbot.org/downloads/#pil"
        sys.exit()


def get_title(path):
    title = path
    if(title[-1:] == "/"):
        title = title[:len(title) - 1]
    title = title.replace("/", "-")
    return title


def make_ncx(title):
    ncx_template = parse("./epubtmp/content.ncx")
    ncx_title = ncx_template.getElementsByTagName('text')[0].childNodes[0]
    ncx_title.data = title
    ncx_label = ncx_template.getElementsByTagName('text')[2].childNodes[0]
    ncx_label.data = title
    f = open("./epubtmp/content.ncx", 'w')
    f.write(ncx_template.toxml())
    f.close()


def make_pages(path, ext):
    page_no = 1
    for infile in sorted(glob.glob(os.path.join(path, '*.' + ext))):
        imgfile = str(page_no) + "." + ext
        shutil.copy(infile, "./epubtmp/" + imgfile)
        # resize
        if options.resize and ext == "jpg":
            size = (options.resize[0], options.resize[1])
            im = Image.open("./epubtmp/" + imgfile)
            # if width > height, display as landscape
            if im.size[0] > im.size[1]:
                im = im.rotate(90)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save("./epubtmp/" + imgfile, "JPEG", quality=75)
        # xml page
        img_template = parse("./epubtmp/page.html")
        img_xml = img_template.getElementsByTagName('img')[0].attributes["src"]
        img_xml.value = imgfile
        f = open("./epubtmp/" + str(page_no) + ".html", 'w')
        f.write(img_template.toxml())
        f.close()
        page_no += 1
    os.remove("./epubtmp/page.html")
    return page_no


def make_opf(title, ext, page_no):
    opf_template = parse("./epubtmp/content.opf")
    opf_title = opf_template.getElementsByTagName('dc:title')[0].childNodes[0]
    opf_title.data = title
    opf_date = opf_template.getElementsByTagName('dc:date')[0].childNodes[0]
    opf_date.data = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    manifest = opf_template.getElementsByTagName('manifest')[0]
    spine = opf_template.getElementsByTagName('spine')[0]

    if ext == "jpg":
        media_type = "image/jpeg"
    elif ext == "png":
        media_type = "image/png"
    else:
        media_type = "application/octet-stream"

    for k in range(1, page_no):
        item = opf_template.createElement('item')
        item.setAttribute("href", str(k) + "." + ext)
        item.setAttribute("id", "added" + str(k))
        item.setAttribute("media-type", media_type)
        manifest.appendChild(item)
        k += 1

    for k in range(1, page_no):
        item = opf_template.createElement('item')
        item.setAttribute("href", str(k) + ".html")
        item.setAttribute("id", "html" + str(k))
        item.setAttribute("media-type", "application/xhtml+xml")
        manifest.appendChild(item)
        k += 1

    for k in range(1, page_no):
        itemref = opf_template.createElement('itemref')
        itemref.setAttribute("idref", "html" + str(k))
        spine.appendChild(itemref)
        k += 1

    f = open("./epubtmp/content.opf", 'w')
    f.write(opf_template.toxml())
    f.close()


# make epub(s)
for path in paths:
    print "Copying Files to Tmp Dir..."
    if os.path.exists("./epubtmp"):
        shutil.rmtree("./epubtmp")
    shutil.copytree("./epub-files", "./epubtmp")

    print "Reading Path : " + path
    title = get_title(path)
    make_ncx(title)
    page_no = make_pages(path, ext)
    make_opf(title, ext, page_no)

    # check output folder
    if not os.path.exists("./output"):
        os.makedirs("output")

    # zip it
    zipfolder.zipper("./epubtmp", "output/" + title + ".epub")
    print "Output file at output/" + title + ".epub"

    # remove Dir
    print "Cleaning Tmp Dir..."
    shutil.rmtree("./epubtmp")
