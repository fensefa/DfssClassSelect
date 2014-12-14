import re
import json
import time
import urllib
import urllib2
import urlparse
import cookielib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pytesser import *
from datetime import date
import os

os.chdir('C://Python27/Lib/site-packages/pytesser')

def getVerify(name):
    #data = urllib2.urlopen(
    im = Image.open(name)
    imgry = im.convert('L')
    text = image_to_string(imgry)
    text = re.sub('\W','',text)
    return text

def urlToString(url):
    data = urllib2.urlopen(url).read()
    f = open('buffer/temp.jpg', 'wb')
    f.write(data)
    f.close()
    return getVerify('buffer/temp.jpg')

def openerUrlToString(opener, url):
    data = opener.open(url).read()
    f = open('buffer/temp.jpg', 'wb')
    f.write(data)
    f.close()
    return getVerify('buffer/temp.jpg')
  
def getOpener(head):
    # deal with the Cookies
    cj = cookielib.CookieJar()
    pro = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

def decodeAnyType(data):
    ret = data
    try:
        temp = data.decode('utf-8')
        ret = temp
    except:
        pass
    try:
        temp = data.decode('gbk')
        ret = temp
    except:
        pass
    try:
        temp = data.decode('gb2312')
        ret = temp
    except:
        pass
    return ret

header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'wsyc.dfss.com.cn',
    'DNT': '1'
}

## the data below are settled by customer to select the class needed
start = 13
end = 17
numid = '3'
year = 2014
month = 12
day = 17
username = '11089212'
password = '235813'

opener = getOpener(header)
url1 = 'http://wsyc.dfss.com.cn/'
url2 = 'http://wsyc.dfss.com.cn/DfssAjax.aspx'
url3 = 'http://wsyc.dfss.com.cn/validpng.aspx?aa=3&page=lg'
url4 = 'http://wsyc.dfss.com.cn/pc-client/jbxx.aspx'
url5 = 'http://wsyc.dfss.com.cn/validpng.aspx'

## try to login until the validcode is right
count = 0
while True:
    print '------------------------'
    print 'have tryed to login %d times, now try again!' % (count)
    count = count + 1
    validcode = openerUrlToString(opener, url3)
    print 'the validcode is ' + validcode
    postDict = {
        'AjaxMethod': 'LOGIN',
        'Account': username,
        'ValidCode': validcode,
        'Pwd': password
    }

    postData = urllib.urlencode(postDict).encode()
    op = opener.open(url2, postData)
    result = op.read().decode('utf-8')
    print 'the result of login is ' + result
    #if result.find('true') >= 0:
    if result == 'true':
        print 'login success!'
        break
    else:
        continue
    

yuechedate = date(year, month, day)
today = date.today()
intervaldays = (yuechedate - today).days
print intervaldays
if intervaldays < 2:
    exit()
validcode = ''
count = 0
## try to select a class until success
while True:
    print '--------------------------'
    print 'have tryed to select %d times, now try again!' % (count)
    count = count + 1
    try:
        validcode = openerUrlToString(opener, url5)
    except:
        continue
    url7 = 'http://wsyc.dfss.com.cn/Ajax/StuHdl.ashx?loginType=2&method=stu'\
           + '&stuid=%s&sfznum=&carid=&ValidCode=%s' % (username, validcode)
    data = opener.open(url7).read().decode('utf-8')
    strs = re.search('\[\{\"fchrdate.*?\}\]', data)
    #print data
    print strs
    if strs is None:
        continue
    jsontext = json.loads(strs.group())
    num = jsontext[intervaldays][numid].split('/')[1]
    print 'remain num is ' + num
    if num == '0':
        print 'no class avaliable!'
        time.sleep(600)
        continue
    try:
        validcode = openerUrlToString(opener, url5)
    except:
        continue
    url6 = 'http://wsyc.dfss.com.cn/Ajax/StuHdl.ashx?loginType=2&method=yueche'\
           + '&stuid=%s&bmnum=BD14101500687&start=%d&end=%d' % (username, start, end)\
           + '&lessionid=001&trainpriceid=BD13040300001&lesstypeid=02'\
           + '&date=%d-%d-%d' % (year, month, day)\
           + '&id=1&carid=&ycmethod=03&cartypeid=01&trainsessionid=0' + numid\
           + '&ReleaseCarID=&ValidCode=' + validcode
    result = opener.open(url6).read().decode('utf-8')
    print 'result of select is ' + result
    if result == 'success':
        print 'select success!'
        break
    else:
        continue
