#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'carpedm20'

from ban import ban
import os
import sys
from f import *
from kakao2 import *
from PIL import Image
from emo import emo
from timeout import timeout
import xml.dom.minidom as minidom
from xgoogle.search import GoogleSearch, SearchError
import mechanize
from contact import contact
#from proxy_list import proxy_list

allow_list = []

BOT_DIR = '/home/carpedm20/bot/'
chatId = ''
#chatId = 55912035628534L
chatId = '' # me
chatId = ''
suc = True
s = start()

HeXA_emo = 5320
HeXA_msg = "HeXA만 사용할 수 있는 명령어 입니다 :)"

#write_pic(s, url=upload_pic('portal.png'), height=1300)
#write_pic(s, url=upload_pic('logo.jpg'), height=300)

#suc = write(s, chatId, "(")
#write_pic(s)
#for i in range(20,30):
#	write_thumb(s, url='11010'+str(i).zfill(2)+'.preview.png')
#write_thumb(s, chatId = chatId, url='1101032.emot_001.gif')
#write_thumb(s, chatId = chatId, url='1101032.preview.png')
#write_thumb(s, msg='이건 헥사봇아니면 못보는 카톡임ㅋ',url='1102211.preview.png')
#write_pic(s, chatId = chatId)

import os

def write_memo(chatId, title, content):
  os.makedirs('memo/'+str(chatId))
  f=open('memo/'+str(chatId)+'memo_'+title+'.txt','a')
  f.write(content+'\n')
  f.close()

def read_memo(chatId, title):
  try:
    f=open('memo/'+str(chatId)+'memo_'+title+'.txt','r')
  except:
    return False

  content = "##" + title + "##\n"
  for index, l in enumerate(f):
    content +="["+str(index)+"] " + l

  return content

def word_filter(arg):
  rp = random.choice(proxy_list)
  proxy = urllib2.ProxyHandler({'http': rp})
  url = "http://translate.google.com/translate_a/t?client=json&hl=en&sl=ko&tl=en&multires=1&otf=2&pc=1&ssel=0&tsel=0&sc=1&text=" + urllib.quote(arg)
  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]
  data = opener.open(url)
  s = data.read()
  j = json.loads(s)

  result = ''

  if j.has_key('dict') is True:
    result = j['dict'][0]['terms'][0]
  #elif j.has_key('sentences') is True:
    #result = j['sentences'][0]['trans']

  if result != '':
    print " [^^^] Word Filter Result From <" + arg + "> To <" + result + ">"
    return result
  else:
    print " [^] Word Filter Result : FAIL ======="
    return False

def word_filter2(arg):
  url = "http://ko.wikipedia.org/w/api.php?action=opensearch&search=" + urllib.quote(arg) + "&format=xml&limit=3"
  dom = minidom.parse(urllib.urlopen(url))
  data = dom.getElementsByTagName('Description')
  if len(data) is 0:
    print " [^] Word Filter Result : FAIL ======="
    return False
  else:
    return arg

@timeout(8)
def pic_down(arg, index = 1, trans = True):
    
    if trans is True:
      #arg = word_filter2(arg)
      arg = word_filter(arg)

    if arg is False:
      return False, False, False

    if index is 1:
        url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&imgsz=middle&rsz=8&q=' + urllib.quote(arg)
    else:
        url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&imgsz=middle&rsz=8&start='+ str((index - 1 )*8) +'&q=' + urllib.quote(arg)
    print "[*] url : " + url
    data = urllib.urlopen(url)
    data = data.read()
    j = json.loads(data)

    if len(j['responseData']['results']) is 0:
        return False, False, False

    d = random.choice(j['responseData']['results'])
    w = d['width']
    h = d['height']
    dir_str = './tmp/'+d['unescapedUrl'].encode('base64')

    link = d['unescapedUrl']
    print link
    urllib.urlretrieve(link, dir_str)
    print ' [#] PIC DOWNLOAD : ' + link

    return dir_str, w, h

while True:
    rooms = get_list(s)

    for r in rooms:
        msg = r['lastMessage']

        command = msg.encode('utf-8').partition(' ')[0][1:]
        chatId = r['chatId']
        """
        if chatId != :
            print "from : " + str(chatId)
            print "command : " + msg
            os.system("python test.py")
        """
        try:
            if msg[0] != '!':
                continue
        except:
            continue

        try:
            test_msg = msg.encode('utf-8')
            arg = msg.encode('utf-8').partition(' ')[2]
        except:
            arg = ""

        if msg == '':
            continue

        if msg[0] == '!': #and chatId == :
            print '===> ' + msg

            if any(word in test_msg for word in ban) is True:
              print " [*] *** Trash *** DETECTED : " + str(chatId) + " : " + test_msg
              result = "금지어가 발견되었습니다 :( "
              result += "\r\n\r\n* 부적절한 사용을 막기 위해 단어 사용을 제한합니다 *"
              rand = random.choice(range(5300,5333))
              write(s, chatId, msg=result)
              continue

            if test_msg.find('헥사봇') != -1 or test_msg.find('핵사봇') != -1:
              print " [*] * HEXABOT * DETECTED : " + str(chatId) + " : " + test_msg
              result = "   [카카오톡 로봇]\r\ndesigned by carpedm20\r\nLink : http://goo.gl/WNZ7k3"
              write(s, chatId, msg=result)
              continue

            # HeXA contact
            if command in contact.keys() and chatId == '':
                w = contact[command]
                try:
                    c = '이름 : %s\r\n닉네임 : %s\r\n기수 : %s\r\n학번 : %s\r\n등급 : %s\r\ne-mail : \r\n%s\r\ntel: %s\r\n비고 : %s' %(command, w['id'], w['class'], w['year'], w['status'], w['email'], w['phone'], w['etc'])
                except:
                    c = '이름 : %s\r\n닉네임 : %s\r\n기수 : %s\r\n학번 : %s\r\n등급 : %s\r\ne-mail : \r\n%s\r\ntel: %s' %(command, w['id'], w['class'], w['year'], w['status'], w['email'], w['phone'])
                write(s,chatId,c)
                continue
            elif command in contact.keys() and chatId != '':
                rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue

            if command in ['헥얼','ㅎㅇ'] and chatId == '':
                photos=os.listdir('./face')
                img = './face/'+photos[random.choice(range(0,len(photos)))]
                i = Image.open(img)
                w, h = i.size
                write_pic(s, chatId=chatId, url=upload_pic(img), height=h, width=w)
                continue
            elif command in ['헥얼','ㅎㅇ'] and chatId != '':
                rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue

            if command in ['한충우','충','ㅊ'] and chatId == '':
                try:
                   i= Image.open('./tmp/'+arg)
                except:
                   img = './tmp/'+str(random.choice(range(1,6)))
                   i = Image.open(img)
                w, h = i.size
                write_pic(s, chatId=chatId, url=upload_pic(img), height=h, width=w)
                continue
            elif command in ['한충우','충','ㅊ'] and chatId != '':
                rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue

            if command in ['헥사진', 'ㅎㅅㅈ','ㅎ'] and chatId == '':
                photos=os.listdir('/home/carpedm20/Dropbox/HeXA_Share/Photo')

                try:
                   img = '/home/carpedm20/Dropbox/HeXA_Share/Photo/' + photos[int(arg)]
                except:
                   num = len(photos)
                   img = '/home/carpedm20/Dropbox/HeXA_Share/Photo/' + photos[random.choice(range(0,num))]
                i = Image.open(img)
                w, h = i.size
                write_pic(s, chatId=chatId, url=upload_pic(img), height=h, width=w)
                continue
            elif command in ['헥사진', 'ㅎㅅㅈ','ㅎ'] and chatId != '':
                rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue

            if command in ['메만', 'ㅁㅁ'] and chatId == '':
                if arg == '':
                    result = "사용법 : !" + command + " (제목) (내용)"
                    result += "\r\n예시 : !" + command + " 야식 피자가짱임"
                    suc = write(s, chatId, result)
                    continue
                else:
                    arg = arg.partition(' ')
                    if arg[2] is '':
                       write(s, chatId, '내용이 없습니다 :(')
                       continue
                    write_memo(arg[0], arg[2])
                    content = read_memo(arg[0])
                    write(s, chatId, content)
            elif command in ['메만', 'ㅁㅁ'] and chatId != '':
                rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue

            if command in ['메보', 'ㅁㅂ'] and chatId == '':
                if arg == '':
                    result = "사용법 : !" + command + " (제목)"
                    result += "\r\n예시 : !" + command + " 야식"
                    suc = write(s, chatId, result)
                    continue
                else:
                    arg = arg.partition(' ')
                    content = read_memo(arg[0])
                    if content is False:
                       write(s, chatId, '그런 메모는 없습니다 :(')
                    else:
                       write(s, chatId, content)
            elif command in ['메보', 'ㅁㅂ'] and chatId != '':
                rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue

            if command in ['메리', 'ㅁㄹ'] and chatId == '':
                files = os.listdir('memo')
                content = "[메모 리스트]\r\n"
                for index, f in enumerate(files):
                    content += '[' + str(index) + '] ' + f.replace('memo_','').replace('.txt','') + '\r\n'
                suc = write(s, chatId, content)
                continue
            elif command in ['메리', 'ㅁㄹ'] and chatId != '':
                rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue

            if command in ['나가','꺼져','ㄲ']:
                leave(s, chatId)
                #write(s,chatId,'즐')
                continue

            if command in ['사진','사','ㅅ','ㅅ1'] and chatId == '':
                if arg == '':
                    result = "사용법 : !" + command + " (검색어)"
                    result += "\r\n예시 : !" + command + " 피자"
                    result += "\r\n\r\n * 부적절한 사용을 막기 위해 검색 기능을 제한합니다 *"
                    suc = write(s, chatId, result)
                    continue
                else:
                    for i in range(1):
                        try:
                            dir_str, w, h = pic_down(arg, trans= False)
                            write_pic(s, chatId=chatId, url=upload_pic(dir_str), height=h, width=w)
                            break
                        except:
                            result = '검색 결과가 없습니다 :('
                            write(s, chatId, result)
                            for e in sys.exc_info():
                                print e
                            continue
                continue

            elif command in ['사진','사','ㅅ','ㅅ1'] and chatId != '':
                if arg == '':
                    result = "사용법 : !" + command + " (검색어)"
                    result += "\r\n예시 : !" + command + " 피자"
                    result += "\r\n\r\n * 부적절한 사용을 막기 위해 검색 기능을 제한합니다 *"
                    suc = write(s, chatId, result)
                    continue
                else:
                    for i in range(1):
                        try:
                            dir_str, w, h = pic_down(arg, trans= True)
                            write_pic(s, chatId=chatId, url=upload_pic(dir_str), height=h, width=w)
                            break
                        except:
                            result = '검색 결과가 없습니다 :('
                            result += "\r\n\r\n * 부적절한 사용을 막기 위해 검색 기능을 제한합니다 *"
                            write(s, chatId, result)
                            for e in sys.exc_info():
                                print e
                            continue
                """rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue"""

            if command in ['ㅅ2','ㅅ3','ㅅ4','ㅅ5','ㅅ6','ㅅ7','ㅅ8','ㅅ9'] and chatId == '':
                if arg == '':
                    result = "사용법 : !" + command + " (검색어)"
                    result += "\r\n예시 : !" + command + " 피자"
                    suc = write(s, chatId, result)
                    continue
                else:
                    index = int(command[3])
                    for i in range(3):
                        try:
                            dir_str, w, h = pic_down(arg, index)
                            write_pic(s, chatId=chatId, url=upload_pic(dir_str), height=h, width=w)
                            break
                        except:
                            write(s, chatId, '검색 결과가 없습니다 :(')
                            for e in sys.exc_info():
                                print e
                            continue
                continue
            elif command in ['ㅅ2','ㅅ3','ㅅ4','ㅅ5','ㅅ6','ㅅ7','ㅅ8','ㅅ9'] and chatId != '':
                rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue

            msg = make_message(msg[1:])

            if command in ['포탈','포','ㅍ'] and chatId == '':
                if arg == '':
                    result = "사용법 : !" + command + " (숫자:공지 순서를 의미)"
                    result += "\r\n예시 : !" + command + " 1"
                    suc = write(s, chatId, result)
                    continue
                else:
                    l = os.listdir(BOT_DIR)
                    bb_list = []

                    for i in l:
                        if i.find('BB') is not -1 and i.find('_') is -1:
                            bb_list.append(i)

                    bb_list.sort()
                    try:
                        target = bb_list[len(bb_list)-int(arg)]
                    except:
                        target = bb_list[len(bb_list) - 1]

                    img = BOT_DIR + target
                    i = Image.open(img)
                    w, h = i.size
                    write_pic(s, chatId=chatId, url=upload_pic(img), height=h, width=w)
                continue
            elif command in ['포탈','포','ㅍ'] and chatId != '':
                rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue

            if command in ['식단','식'] and chatId == '':
                if arg == '':
                    result = "사용법 : !" + command + " (숫자:식단 순서를 의미)"
                    result += "\r\n예시 : !" + command + " 1"
                    suc = write(s, chatId, result)
                    continue
                else:
                    l = os.listdir(BOT_DIR)
                    bb_list = []

                    for i in l:
                        if i.find('food_') is not -1 and i.find('.png_') is not -1:
                            bb_list.append(i)

                    bb_list.sort()

                    try:
                        target = bb_list[len(bb_list)-int(arg)]
                    except:
                        target = bb_list[len(bb_list) - 1]

                    img = BOT_DIR + target
                    print img
                    i = Image.open(img)
                    w, h = i.size
                    write_pic(s, chatId=chatId, url=upload_pic(img), height=h, width=w)
                continue
            elif command in ['식단','식'] and chatId != '':
                rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue

            if command in ['랜덤','ㄹ'] and chatId == '':
                try:
                    write_thumb(s, chatId, url=emo[int(arg)])
                except:
                    write_thumb(s, chatId, url=random.choice(emo))
                continue
            elif command in ['랜덤','ㄹ'] and chatId != '':
                rand = random.choice(range(5300,5333))
                write_thumb(s, chatId, msg=HeXA_msg, url = emo[int(rand)])
                continue

            else:
	        try:
	            if msg.find(u'휴대폰을 보면 지금도 남아있는') != -1:
		        suc = write(s, chatId, '(궁금)')
		        suc = write(s, chatId, '(흡족)')
		        suc = write(s, chatId, '(윙크)')
		        suc = write(s, chatId, '(크크)')
	        except:
		    z=123
            suc = write(s, chatId, msg)
        #else:
            #suc = read(s, chatId)

    if suc is False:
	print "[#] Socket dead!!"
	s = start()
	suc = True
