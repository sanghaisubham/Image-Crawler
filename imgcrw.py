import urllib2
import urllib
import os
import re
import MySQLdb
import Image

count =2
dirpath='E:\image'

try:
    db=MySQLdb.connect("127.0.0.1","root","root","imgcrawl")
    c1=db.cursor()
except Exception: print'Connection error'


def func(urla):
    global c1
    global count
    try:
        html=urllib.urlopen(urla)
        imgread(urla)
        lines=html.readlines()
        for line in lines:
            pat=r'<a.*href="(https?:[\w\s!#$%&()*+,\-./:;<=>?@[\\\]^_`{|}~]*)'
            m=re.findall(pat,line)
            if m:
                try:
                    c1.execute("""INSERT INTO url_tra(url_name)VALUES(%s)""",m[0])
                    print m[0]
                except Exception: st=1
        try:
            c1.execute("""SELECT url_name FROM url_tra WHERE id=(%s)""",(count))
            rs=c1.fetchone()
            count=count+1
            if count>100: return 0
            else: func(rs[0])
        except Exception: print "data reading error"
    except IOError,e: print 'url cannot be retrieved: '+str(e)


def imgdwn(url,filename):
    try:
        path=os.path.join(dirpath,filename)
        im=urllib.urlretrieve(url,path)
    except:
        print 'image cannot be found'


def imgread(urlx):
    html=urllib.urlopen(urlx)
    lines=html.readlines()
    for line in lines:
        pattern=r'<a.*href="[\w\s!#$%&()*+,\-./:;<=>?@[\\\]^_`{|}~]*.*img'
        match=re.search(pattern,line)
        if match:
            print 'match found'
            pat=r'<a.*href="(https?:[\w\s!#$%&()*+,\-./:;<=>?@[\\\]^_`{|}~]*)'
            pat1=r'<img.*src="([\w\s!#$%&()*+,\-./:;<=>?@[\\\]^_`{|}~]*)'
            pat2=r'<img.*alt="([\w\s!#$%&()*+,\-./:;<=>?@[\\\]^_`{|}~]*)'
            m=re.findall(pat,line)
            m1=re.findall(pat1,line)
            m2=re.findall(pat2,line)
            M=''
            M1=''
            M2=''
            err=0
            if(m) : print 'm[0]= ' + str(m[0])
            if(m1) : print 'm[1]= ' + str(m1[0])
            if(m2) : print 'm[2]= ' + str(m2[0])
            if m or m1 or m2:
                if m: M=str(m[0])
                if m1:
                    M1=str(m1[0])
                else : continue
                if m2:
                    M2=str(m2[0])
                    tstr=r'protected'
                    m3=re.findall(tstr,M2)
                    if(m3):
                        err=1
                        print 'error found'
                if err==0:
                    print 'inserted'
                    imgext1(urlx,M,M1,M2)
            
def imgext1(intiurl,imglink,src,alt):
    global c1
    s=src.split('/')
    for img in s: img
    if not src.startswith('http'): src=intiurl+'/'+src
    imgdwn(src,img)
    image=Image.open(img)
    im=image.size
    try:
        c1.execute("""INSERT INTO image(inti_url,imglink,imgname,imgsrc,height,width,alt)VALUES(%s,%s,%s,%s,%s,%s,%s)""",(intiurl,imglink,img,src,str(im[1]),str(im[0]),alt))
    except:
        print 'DUPLICATE IMAGE'
    
if not(os.path.isdir(dirpath)): os.mkdir(dirpath)
os.chdir(dirpath)

url='http://www.quora.com/Celebrities/What-celebrity-do-you-just-want-to-punch-in-the-face'
try:
    c1.execute("""INSERT INTO url_tra(url_name)VALUES(%s)""",url)
except Exception: st=1
func(url)
