import sys,time
reload(sys)
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup
import urllib2, urllib
from json import *

cookie = "__jdv=76161171|baidu|-|organic|%E4%BA%AC%E4%B8%9C|1638788911469; cud=190a3859dc5fcccce4868aa089fac6a8; cvt=1; __jdu=163878891146755421046; areaId=1; ipLoc-djd=1-2802-0-0; PCSYCityID=CN_110000_110100_110111; pinId=e1x2UyFyli-zfUvE9n0Rlw; pin=zhaoxiaqian; unick=细腿VS蛮腰; ceshi3.com=103; _tp=qB0FXbODznCLfsfMlQbe4Q==; _pst=zhaoxiaqian; shshshfp=3605e221c261841874a6c4a64eab3591; shshshfpa=c93e9c09-03e3-320d-8b8c-d982e6837648-1638788997; shshshfpb=zt5v93xfweiCTpfAFB0+cGg==; user-key=a763eab6-c752-4825-8119-cfe813740e46; __jda=122270672.163878891146755421046.1638788911.1638788911.1638788911.1; __jdc=122270672; thor=A066E6F4B8E43559048C4D9FB07C9912D285E834DF4340D9C03C1F82BEF70212A27C1F345D4693460E96118EB9C6C345CFF06BAB8D6FC00CB9ED1E4702B3A0653AA2C6AB9DB84ADE37365E3CE9EBABA07D8D8D861CFB65EE29E64D26788E985B7BD6EF8B10F6F0EBC7149B3B3892FCC56A2B110105EC8FC08C8B148DD459638D43C2E5A9354D831C90A02DF4F1E137C3; 3AB9D23F7A4B3C9B=Z4AODMYHSDOGUK6CDTBTCXABFV6ZOK72QRFPAGCIREIEFJKUH3LGEGN6IH2GC76AE4GPUUQC6TQM4PNNOYMFVWO7JY; csn=10; __jdb=122270672.11.163878891146755421046|1.1638788911"

def foo(actid): 
    f = urllib2.Request(
        url     = 'http://try.jd.com/migrate/apply?activityId='+actid+'&source=0',
        )
    f.add_header('Cookie', cookie);
    response = urllib2.urlopen(f)
    g = response.read()
    print g.decode('UTF-8','ignore')
    return 0

def foo2(actList): 
    f = urllib2.Request(
        url     = 'http://try.jd.com/user/getApplyStateByActivityIds?activityIds=' + ','.join(actList),
        )
    f.add_header('Cookie', cookie);
    f.add_header('Referer','http://try.jd.com/activity/getActivityList?page=1&activityState=0')
    response = urllib2.urlopen(f)
    g = response.read()
    d=JSONDecoder().decode(g)
    actlist2 = []
    for i in d:
        actlist2.append(str(i['activityId']))
    return set(actList) - set(actlist2)
    
def foo3(page): 
    f = urllib2.Request(
        url     = 'http://try.jd.com/activity/getActivityList?page='+str(page)+'&activityState=0',
        )
    response = urllib2.urlopen(f)
    d = response.read()
    soup = BeautifulSoup(d)

    actList = []
    for lind in soup.find_all('li'):
        actid = lind.get('activity_id')
        if actid:
            actList.append(str(actid))

    return actList
    
def foo4(): 
    f = urllib2.Request(
        url     = 'http://try.jd.com/activity/getActivityList?activityState=0',
        )
    response = urllib2.urlopen(f)
    d = response.read()
    soup = BeautifulSoup(d)

    count = 0
    start =  str(soup.head.script).find('{')
    end = str(soup.head.script).rfind('}') + 1
    jsonStr = str(soup.head.script)[start:end]
    jsonStr = jsonStr.replace('\'', "\"")

    d=JSONDecoder().decode(jsonStr)
    return d["pagination"]["pages"]

total = foo4()

for i in xrange(total+1):
    print i
    actList = foo3(i)
    actList = foo2(actList)
    for actid in actList:
        foo(actid)
        time.sleep(5)
print 'end'
while True:
    pass
