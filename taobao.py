#coding: utf-8
import sys
import re
import os
#import httplib2
import urllib2
import cookielib
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

cj = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(handler,urllib2.HTTPHandler)
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36')]
opener.addheaders.append(('Pragma', 'no-cache'))
opener.addheaders.append(('cache-control', 'no-cache'))

urllib2.install_opener(opener)

outbase = 'download'
fenge = '/'

def getshopdomain(url):
	domainx = re.findall('http[s]{0,1}://(.*?)/',url)
	return domainx[0]

def getpids(url,shop):
	#print url
	html = None
	html = urllib2.urlopen(url).read()
	pageprex = re.findall('(http[s]{0,1}://.*?)/',url)
	#print pageprex
	pagetrueurlx = re.findall('J_ShopAsynSearchURL.*?value="(.*?)"',html)
	#print pagetrueurlx
	pagetrueurl = pageprex[0]+re.compile('&amp;').sub('&',pagetrueurlx[0])
	#print pagetrueurl
	html2 = urllib2.urlopen(pagetrueurl).read()
	#print html2
	pidsx = re.findall('J_TGoldData.*?href=\\\\"(.*?)\\\\',html2)
	for pidurldump in pidsx:
		pidurl = re.compile('^//').sub('http://',pidurldump)
		getpimg(pidurl,shop)

def getpimg(pidurl,shop):
	outdir = outpath(pidurl,shop)
	html = urllib2.urlopen(pidurl).read()
	pdurlx = re.findall('descUrl.*?(//.*?)\'',html)
	pdurl = re.compile('^//').sub('http://',pdurlx[0])
	#print pdurlx

	pimgx = re.findall('J_UlThumb[\s\S]*?ul>',html)
	pimgx = re.findall('img.*?="(.*?)_\d*x\d*',pimgx[0])
	#print pimgx
	for pimg in pimgx:
		pimg = re.compile('^//').sub('http://',pimg)
		downcmd(pimg,outdir)

	getpdimg(pdurl,outdir)

def getpdimg(pdurl,outdir):
	html = urllib2.urlopen(pdurl).read()
	pimgx = re.findall('<img.*?src="(.*?)"',html)
	for pimg in pimgx:
		pimg = re.compile('^//').sub('http://',pimg)
		downcmd(pimg,outdir)

def outpath(pidurl,shop):
	outdirx = re.findall('id=(\d*)',pidurl)
	outdir = outbase+fenge+shop+fenge+outdirx[0]+fenge
	#print outdir
	if not os.path.exists(outdir):
		os.makedirs(outdir)
	return outdir

def downcmd(imgurl,outdir):
	#print "downlaod the imgfile :%s out to %s" % (imgurl, outdir)

	filePath = outdir + os.path.basename(imgurl)
	#print imgurl
	try:
		pic = urllib2.urlopen(imgurl)
	except urllib2.URLError,e:
		#if e.code == '404':
		print imgurl
		sys.stdout.write("\b*>")
	else:
		with open(filePath, 'wb') as localFile:
			localFile.write(pic.read())
		sys.stdout.write("\b=>")
	pass

def main(urlstr,b,e):
	shop = getshopdomain(urlstr)
	for i in range(b,e+1):
		url = urlstr % i
		print ''
		print url
		getpids(url,shop)

main('https://shop35467425.taobao.com/search.htm?pageNo=%s',1,4)
#getpids('https://blog.iuxs.info','ss')
