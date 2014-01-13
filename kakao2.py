__author__ = 'carpedm20'
# -*- coding: utf-8 -*-
import mechanize
import cookielib
import simplejson as json
import time
import re
import os, sys
import urllib2
import random
import atexit
import urllib
import xml.dom.minidom as minidom
import datetime
import smtplib
from twitter import *
from say import say
from ban import ban
#from proxy_list import proxy_list

success_ip = ''
jsession = ''

COMMAND = {}
COMMAND['HELP'] = ['헬프','도움','헬','']
COMMAND['COMMAND'] = ['명령어','명',]
COMMAND['STATUS'] = ['상태','상']
COMMAND['UPDATE'] = ['업데이트','업']
COMMAND['EXIT'] = ['나가','꺼져','ㄲ']

COMMAND['CREATOR'] = ['만든놈']
COMMAND['HEXA'] = ['헥사','HeXA']

#COMMAND['PORTAL'] = ['포탈','포','ㅍ']
#COMMAND['FOODTABLE'] = ['식단','식','ㅅ']
COMMAND['BUS'] = ['버스','버','ㅂ']
COMMAND['FOOD'] = ['야식','배달','배']

#COMMAND['KO_DIC'] = ['영한','한','ㅎ']
COMMAND['WEATHER'] = ['날씨','날','ㄴ']
COMMAND['WEATHER_TOMORROW'] = ['내일날씨']
COMMAND['SEARCH_RANK'] = ['실시간','실']
COMMAND['SAY'] = ['명언','명','ㅁ']
COMMAND['PIC'] = ['사진','사','ㅅ']
COMMAND['YOUTUBE'] = ['유투브','유']
COMMAND['WIKI'] = ['위키','위']

COMMAND['DICE'] = ['주사위','주','ㅈ']
COMMAND['ROCK'] = ['가위바위보','짱깸뽀']
COMMAND['TALK'] = ['야','너','ㅇ']

COMMAND['MEMO_WRITE'] = ['메만','ㅁㅁ']
COMMAND['MEMO_READ'] = ['메보','ㅁㅂ']
COMMAND['MEMO_LIST'] = ['메리','ㅁㄹ']

command_list = [COMMAND[c][0] for c in COMMAND]
command_list_str = ''

for c in command_list:
    command_list_str += c + ', '

command_list_str = command_list_str[:len(command_list_str)-2]

total_command_list_str = ''

total_command_list = [COMMAND[c] for c in ['HELP','COMMAND','STATUS','UPDATE','EXIT']]
total_command_list_str += '  [헥사봇]\r\n'

for t in total_command_list:
    current_str = ' - '
    for c in t:
        current_str += c + ', '
    total_command_list_str += current_str[:len(current_str)-2] + '\r\n'

total_command_list = [COMMAND[c] for c in ['CREATOR','HEXA']]
total_command_list_str += '\r\n  [제작자]\r\n'

for t in total_command_list:
    current_str = ' - '
    for c in t:
        current_str += c + ', '
    total_command_list_str += current_str[:len(current_str)-2] + '\r\n'

total_command_list = [COMMAND[c] for c in ['BUS','FOOD']]
total_command_list_str += '\r\n  [UNIST]\r\n'

for t in total_command_list:
    current_str = ' - '
    for c in t:
        current_str += c + ', '
    total_command_list_str += current_str[:len(current_str)-2] + '\r\n'

total_command_list = [COMMAND[c] for c in ['WIKI','WEATHER','WEATHER_TOMORROW','SEARCH_RANK','SAY','PIC','YOUTUBE']]
total_command_list_str += '\r\n  [검색]\r\n'

for t in total_command_list:
    current_str = ' - '
    for c in t:
        current_str += c + ', '
    total_command_list_str += current_str[:len(current_str)-2] + '\r\n'

total_command_list = [COMMAND[c] for c in ['MEMO_WRITE','MEMO_READ','MEMO_LIST','DICE','ROCK','TALK']]
total_command_list_str += '\r\n  [기타]\r\n'

for t in total_command_list:
    current_str = ' - '
    for c in t:
        current_str += c + ', '
    total_command_list_str += current_str[:len(current_str)-2] + '\r\n'

total_command_list_str = total_command_list_str[:len(total_command_list_str)-2]

COMMAND['CREATOR'] = ['만든이','만든놈','김태훈','carpedm20']
COMMAND['PORTALBOT'] = ['포탈봇']
COMMAND['FOODBOT'] = ['식단봇']
COMMAND['HEXABOT'] = ['헥사봇']
COMMAND['ROBOT'] = ['로봇']
COMMAND['MOZOKILLER'] = ['모조킬러']

def make_message(msg, name=''):
    global success_ip, jsession
    msg = msg.encode('utf-8')
    command = msg.partition(' ')[0]
    print " COMMAND : " + command

    try:
        arg = msg.partition(' ')[2]
        print " ARG : " + command

    except:
        arg = ""

    if command in COMMAND['HELP']:
        result = "!(느낌표) + \r\n" + command_list_str + " 등\r\n\r\n"
        result += "예시: !버스 133\r\n"
        result += "예시: !유니스트 (기본 검색)\r\n\r\n"
        result += "힌트 : !명령어\r\n"
        result += "* 헥사봇은 가장 아래의 명령어만 읽습니다 *\r\n\r\n"
        result += "만든이 : 김태훈(carpedm20)"
        result += "\r\nHeXA : http://hexa.us.to"

    elif command in COMMAND['COMMAND']:
        result = ''
        result += total_command_list_str

    elif command in COMMAND['SEARCH_RANK']:
        url = 'http://openapi.naver.com/search?key=&query=nexearch&target=rank'

        dom = minidom.parse(urllib.urlopen(url))
        data = dom.getElementsByTagName('K')
        status = dom.getElementsByTagName('S')

        result = ' - 실시간 급상승 검색어 -\r\n\r\n'

        for idx, d in enumerate(data):
            print d.nodeValue
            result += '['+str(idx+1)+'] '+ d.firstChild.nodeValue.encode('utf-8') + ' ' + status[idx].firstChild.nodeValue.encode('utf-8').replace('+','▲').replace('-','▼') + '\r\n'

        result = result[:len(result)-2]        

    elif command in COMMAND['TALK']:
        if arg == "":
            result = "사용법 : !" + command + " (하고싶은 말)"
            result += "\r\n예시 : !" + command + " 안녕"
            result += "\r\n\r\n※ 욕설과 같은 부적절한 대답을 할 수 있습니다. 이것은 제작자가 의도한 것이 아닙니다"
            return result

        if any(word in arg for word in ban) is True:
           result = "금지어가 발견되었습니다 :( "
           result += "\r\n\r\n* 부적절한 사용을 막기 위해 단어 사용을 제한합니다 *"
           result += "\r\n\r\n※ 욕설과 같은 부적절한 대답을 할 수 있습니다. 이것은 제작자가 의도한 것이 아닙니다"
           return result
                return
    elif command in COMMAND['SAY']:
        result = ' - 오늘의 명언 -\r\n'
        try:
            s = say.keys()[int(arg)]
        except:
            s = random.choice(say.keys())
        result = say[s] + " : \r\n" + s

    elif command in COMMAND['STATUS']:
        now = time.localtime()
        result = "[" + str(now.tm_year) + "." + str(now.tm_mon) +"." + str(now.tm_mday) + " " + str(now.tm_hour) + ":" + str(now.tm_min) + ":" + str(now.tm_sec) + "]\r\n활동하고 있는 헥사봇 수 : " + str(random.choice(range(500,510)))
    
    elif command in COMMAND['HEXA']:
        result = "2011년에 만들어진 UNIST의 컴퓨터 정보보안 동아리인 HeXA는 Hacker's eXciting Academy의 약자이며, "
        result += "컴퓨터 보안에 대한 깊은 연구에 관심을 두고 있는 동아리 입니다."
        result += "\r\n\r\n* http://hexa.us.to"
        result += "\r\n* https://www.facebook.com/unist.hexa"
    
    elif command in COMMAND['UPDATE']:
        result = "[2013.06.27]\r\n"
        result += " * 베타 서비스 시작\r\n"
        result += "[2013.07.06]\r\n"
        result += " * 베타 서비스 종료\r\n"
        result += "[2013.08.06]\r\n"
        result += " * 정식 서비스 시작\r\n"
        result += " - !사진 추가\r\n"
        result += " - !포탈 추가\r\n"
        result += " - !식단 추가\r\n"
        result += " - !나가 추가\r\n"
        result += " - !실시간 추가\r\n"
        result += " - 검색 기능 강화\r\n"
        result += "[2013.08.17]\r\n"
        result += " * 정식 서비스 종료\r\n"
        result += "[2013.09.16]\r\n"
        result += " - !메만 추가\r\n"
        result += " - !메리 추가\r\n"
        result += " - !메보 추가\r\n"
        result += "[2013.09.20]\r\n"
        result += " - !헥사진 추가\r\n"
        result += " - !헥얼 추가\r\n"
        result += "[2013.10.14]\r\n"
        result += " * 2차 서비스 시작\r\n"
        result += " - 일부 명령어 제한\r\n"
        result += "[2013.11.06]\r\n"
        result += " - 안정화 기능 추가\r\n"
        result += "[2013.11.09]\r\n"
        result += " - !사진 복구 및 제한\r\n"
        result += " - !야 및 !너 단어 제한\r\n"
        result += "[2014.01.09]\r\n"
        result += " - !메만,메리,메보 누구나 사용 가능\r\n"
        result += " - 속도 개선\r\n"
        result += "\r\n현재 버전 : 3.7.1"
    
    elif command in COMMAND['YOUTUBE']:
        result = '수정중입니다 :)'
        return result

        if arg == "":
            result = "사용법 : !" + command + " (검색어)"
            result += "\r\n예시 : !" + command + " 물음표"
        else:
            result = ""

            url = "http://gdata.youtube.com/feeds/api/videos?q=" + urllib.quote(arg) + "&max-results=3&alt=jsonc&v=2"

            data = urllib2.urlopen(url)
            #data=data.read().replace('\\x','').replace(',200,null)','').replace('dict_api.callbacks.id100(','')

            j = json.load(data)

            try:
                data = j['data']['items']
            except:
                result = "검색 결과가 없습니다 :("
                return result

            if len(data) is 0:
                result = "검색 결과가 없습니다 :("
            else:
                for idx, d in enumerate(data):
                    result += '[' + str(idx+1) + '] ' + d['title'] + "\r\n" + d['content']['5'] + '\r\n\r\n'
                result = result[:len(result)-4]

    elif command in COMMAND['BUS']:
        result = ""

        if True:
            #result = "공사중"
        #else:
          if arg == "":
            result = "사용법 : !" + command + " (133,233,733,337 중 1)"
            #esult += "\r\n예시 : !" + command + " 233"
            result += "\r\ninfo : http://unif.wo.tc/"
          else:
            url = 'http://unif.wo.tc/'
            r = urllib2.urlopen(url)
            r = r.read()

            r = r.replace('<br />','\n').replace('<br/>','\n').replace('</br />','\n').replace('</br>','\n')
            r = r.split('\n')

            visited = False

            for l in r:
                if l.find('133번') is not -1 and arg == '133':
                    result += l.strip()# + '\r\n'
                elif l.find('233번') is not -1 and arg == '233':
                    result += l.strip()# + '\r\n'
                elif l.find('733번') is not -1 and arg == '733':
                    result += l.strip()# + '\r\n'
                elif l.find('(시내)') is not -1 and arg == '337':
                    result += l.strip() + '\r\n'
                elif l.find('(KTX)') is not -1 and arg == '337':
                    result += l.strip() + '\r\n'
                elif l.find('337번') is not -1 and arg == '337':
                    if visited == False:
                        visited = True
                        result += l.strip() + '\r\n'
                    else:
                        result += l.strip()

                if arg not in ['133','233','733','337']:
                    result = "버스 번호가 잘못되었습니다 :("
          try:
            result.decode('utf8')
          except:
            result = arg + '번 현재 운행 종료되었습니다'

    elif command in COMMAND['FOOD']:
        if arg == "중국집" or arg == "중국" or arg == "짜장" or arg == "짬뽕" or arg == "탕수육":
            result = '      - 오늘의 중국집 -\r\n'
            name = random.choice(FOOD[0].keys())
            result += "" + name + ' : ' + FOOD[0][name]
        elif arg == "치킨집" or arg == "치킨" or arg == "통닭" or arg == "칙" or arg == "닭" or arg == "칰" or arg == "닥":
            result = '      - 오늘의 치킨 -\r\n'
            name = random.choice(FOOD[1].keys())
            result += "" + name + ' : ' + FOOD[1][name]
        elif arg == "피자집" or arg == "피자" or arg == "피짜":
            result = '      - 오늘의 피자 -\r\n'
            name = random.choice(FOOD[2].keys())
            result += "" + name + ' : ' + FOOD[2][name]
        elif arg == "족발집" or arg == "족발":
            result = '      - 오늘의 족발 -\r\n'
            name = random.choice(FOOD[3].keys())
            result += "" + name + ' : ' + FOOD[3][name]
        elif arg == "돈까스집" or arg == "돈까스" or arg == "돈가스" or arg == "돈가스집":
            result = '      - 오늘의 돈까스 -\r\n'
            name = random.choice(FOOD[4].keys())
            result += "" + name + ' : ' + FOOD[4][name]
        else:
            find = False
            result = ""

            for f in TOTAL_FOOD:
                if f.find(arg) is not -1:
                    find = True
                    result += f + " : " + TOTAL_FOOD[f] + "\r\n"

            result=result[:result.rfind('\r\n$')]

            if find is False or arg == "":
                result = "사용법 1 : !" + command + " (중국집, 치킨, 피자, 족발, 돈까스 중 1)"
                result += "\r\n예시 : !" + command + " 치킨"
                result += "\r\n\r\n사용법 2 : !" + command + " (검색어)"
                result += "\r\n예시 : !" + command + " 치"

    elif command in COMMAND['WEATHER']:
        example = False

        if arg == "서울":
            result = "     - 오늘의 서울 날씨 - \r\n"
            url = 'http://www.kma.go.kr/wid/queryDFS.jsp?gridx=11&gridy=84'
        elif arg == "부산":
            result = "     - 오늘의 부산 날씨 - \r\n"
            url = 'http://www.kma.go.kr/wid/queryDFS.jsp?gridx=26&gridy=84'
        elif arg == "대구":
            result = "     - 오늘의 대구 날씨 - \r\n"
            url = 'http://www.kma.go.kr/wid/queryDFS.jsp?gridx=27&gridy=84'
        elif arg == "인천":
            result = "     - 오늘의 인천 날씨 - \r\n"
            url = 'http://www.kma.go.kr/wid/queryDFS.jsp?gridx=28&gridy=84'
        elif arg == "광주":
            result = "     - 오늘의 광주 날씨 - \r\n"
            url = 'http://www.kma.go.kr/wid/queryDFS.jsp?gridx=29&gridy=84'
        elif arg == "대전":
            result = "     - 오늘의 대전 날씨 - \r\n"
            url = 'http://www.kma.go.kr/wid/queryDFS.jsp?gridx=30&gridy=84'
        elif arg == "제주":
            result = "     - 오늘의 제주 날씨 - \r\n"
            url = 'http://www.kma.go.kr/wid/queryDFS.jsp?gridx=50&gridy=84'
        elif arg == "?":
            result = "사용법 : !" + command + " (울산,서울,부산,대구,인천,광주,대전,제주 중 1)"
            result = "\r\n예시: !" + command + " 대구"
        else:
            result = "     - 오늘의 울산 날씨 - \r\n"
            url = 'http://www.kma.go.kr/wid/queryDFS.jsp?gridx=98&gridy=84'
            example = True

        result += '\r\n'
        dom = minidom.parse(urllib.urlopen(url))
        num = len(dom.getElementsByTagName('hour'))
        #for i in range(6)):
        for i in range(num):
            hour = dom.getElementsByTagName('hour')[i].firstChild.nodeValue.encode('utf-8')
            temp = dom.getElementsByTagName('temp')[i].firstChild.nodeValue.encode('utf-8')
            wfKor = dom.getElementsByTagName('wfKor')[i].firstChild.nodeValue.encode('utf-8')
            day = dom.getElementsByTagName('day')[i].firstChild.nodeValue.encode('utf-8')

            if len(hour) is 1:
                if day == '2':
                    break
                hour = hour.zfill(2)
                result += hour + '시 : ' + wfKor + " (" + temp + '℃)\r\n'
            else:
                result += hour + '시 : ' + wfKor + " (" + temp + '℃)\r\n'

        result = result[:len(result)-2]
        if example is True:
            result += "\r\n\r\n예시 : !" + command + " 대구\r\n(울산,서울,부산,대구,인천,광주,대전,제주 중 1)"

    elif command in COMMAND['CREATOR']:
        result = "김태훈(1992년 ~)은 UNIST 전기전자컴퓨터공학부의 학부생이다. 3대 HeXA 회장이며 헥사봇,포탈봇,식단봇,모조킬러,로봇 등의 프로그램을 만들었다."
        result += "\r\n\r\n contact : "
        result += "\r\n - http://carpedm20.us.to"
        result += "\r\n - carpedm20@gmail.com"
        result += "\r\n\r\ninfo : !헥사봇, !포탈봇, !식단봇, !모조킬러, !로봇"

    elif command in COMMAND['MOZOKILLER']:
        result = "   [모조 킬러]\r\ndesigned by carpedm20\r\nLink : https://www.facebook.com/photo.php?fbid=518049918286670"

    elif command in COMMAND['HEXABOT']:
        result = "   [카카오톡 로봇]\r\ndesigned by carpedm20\r\nLink : http://goo.gl/WNZ7k3"
        #result = "   [카카오톡 로봇]\r\ndesigned by carpedm20\r\nLink : https://www.facebook.com/photo.php?fbid=486965651395097"

    elif command in COMMAND['PORTALBOT']:
        result = "   [포탈 공지 자동 업로드]\r\nDesigned by carpedm20\r\nLink : http://www.facebook.com/hexa.portal"

    elif command in COMMAND['FOODBOT']:
        result = "   [학교 식단 자동 업로드]\r\nDesigned by carpedm20\r\nLink : http://www.facebook.com/hexa.food.bot"

    elif command in COMMAND['ROBOT']:
        result = "   [포탈 공지 및 BB 뷰어]\r\nDesigned by carpedm20\r\nLink : http://carpedm20.blogspot.kr/2013/03/robot.html"

    elif command in COMMAND['DICE']:
        result = ''

        if arg != "" and isInt(arg) is True:
            if 999999 > int(arg) > 0:
                num = random.randint(1, int(arg))
                result += str(num) + " \r\n(범위 : 1 ~ " + str(arg) + ")"
            else:
                num = random.randint(1, 10)
                result += str(num) + " \r\n(기본 : 1 ~ 10)"
        else:
            num = random.randint(1, 10)
            result += str(num) + " \r\n(기본 : 1 ~ 10)\r\n사용법 : !주사위 (큰숫자)"
            result += "\r\n예시 : !" + command + " 6"

    elif command in COMMAND['ROCK']:
        print "[*] rock scissors paper"

        result = ''
        choice = random.choice(['가위','바위','보'])
        result += "[헥사봇] : " + choice + "\r\n"

        win = ["이기셨습니다 :^)","승리~",'승리하셨습니다 :)','승리!']
        lose = ["패배하셨습니다 :(","패배!",'졌습니다 :(','패배~']
        same = ['비기셨습니다 :|','비김!','비김! 다시 도전하세요 :)']

        if arg != "" and arg in ['가위','바위','보','묵','찌','빠','보자기','주먹']:
            if arg in ["가위",'찌'] and choice in ["보","보자기"]:
                result += random.choice(win)
            elif arg in ["가위",'찌'] and choice in ["바위","묵","주먹"]:
                result += random.choice(lose)
            elif arg in ["바위","묵","주먹"] and choice in ["가위",'찌']:
                result += random.choice(win)
            elif arg in ["바위","묵","주먹"] and choice in ["보","보자기"]:
                result += random.choice(lose)
            elif arg in ["보","보자기"] and choice in ["바위","묵","주먹"]:
                result += random.choice(win)
            elif arg in ["보","보자기"] and choice in ["가위",'찌']:
                result += random.choice(lose)
            elif arg in ["보","보자기"] and arg in ["보","보자기"]:
                result += random.choice(same)
            elif arg in ["바위","묵","주먹"] and arg in ["바위","묵","주먹"]:
                result += random.choice(same)
            elif arg in ["가위",'찌'] and arg in ["가위",'찌']:
                result += random.choice(same)
        else:
            if command == "가위바위보" or command == "짱깸뽀":
                result = "사용법 : !" + command + " (가위,바위,보 중 1)"
                result += "\r\n예시 : !" + command + " 바위"

    elif command in COMMAND['MEMO_READ']:
        return False
    elif command in COMMAND['MEMO_WRITE']:
        return False
    elif command in COMMAND['MEMO_LIST']:
        return False
    elif command in COMMAND['PIC']:
        return False
    elif command in COMMAND['EXIT']:
        return False
    elif command in COMMAND['WIKI']:
        print "hello"
        if arg == "":
            result = "사용법 : !" + command + " (검색어)"
            result += "\r\n예시 : !" + command + " 유니스트"
            return result

        if len(re.findall('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', arg)) is not 0:
            url = "http://ko.wikipedia.org/w/api.php?action=opensearch&search=" + urllib.quote(arg) + "&format=xml&limit=3"
        else:
            en = True
            url = "http://en.wikipedia.org/w/api.php?action=opensearch&search=" + str(arg) + "&format=xml&limit=3"

        dom = minidom.parse(urllib.urlopen(url))

        data = dom.getElementsByTagName('Description')

        result = ''
        count = 1

        if len(data) is 0:
            result += ""
            result += "검색 결과가 없습니다"
            result += " " + random.choice(EMOTICON)
            #result += "\r\n참고 : !헬프"

        else:
            for idx, d in enumerate(data):
                try:
                    result += '[' + str(idx + 1) + '] ' + d.firstChild.nodeValue.encode('utf-8') + '\r\n\r\n'
                except:
                    continue
            result = result[:len(result) - 4]

    else:
        print "!!!!!!!!!!!!!!!"
        if len(re.findall('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', msg)) is not 0:
            url = "http://ko.wikipedia.org/w/api.php?action=opensearch&search=" + urllib.quote(msg) + "&format=xml&limit=3"
        else:
            en = True
            url = "http://en.wikipedia.org/w/api.php?action=opensearch&search=" + str(msg) + "&format=xml&limit=3"

        dom = minidom.parse(urllib.urlopen(url))

        data = dom.getElementsByTagName('Description')

	result = ''
        count = 1

        if len(data) is 0:
            result += ""
            result += random.choice(["모르는 명령어입니다","어려워요","어렵습니다","이해할 수 없습니다","읭?","모릅니다","...","모르겠습니다","몰라요"])
            result += " " + random.choice(EMOTICON)
            result += "\r\n참고 : !헬프"

        else:
            for idx, d in enumerate(data):
                try:
                    result += '[' + str(idx + 1) + '] ' + d.firstChild.nodeValue.encode('utf-8') + '\r\n\r\n'
                except:
                    continue
            result = result[:len(result) - 4]
            """
            for i in range(3):
                d = random.choice(data)
                v = d.firstChild.nodeValue.encode('utf-8')

                result += v
                break
            """
    print result
    return result


FOOD = [{'황제 쟁반 짜장':'052-211-0565/3050', '황궁 쟁반 짜장':'052-248-2500','도원 홍합 짬뽕':'052-248-2770',
        '금향 쟁반짜장':'052-211-9550', '만선':'052-211-9339','해성':'052-211-0042','오마이 짬뽕':'052-244-0207',
        '탕코':'052-211-9934','탕수육 코리아':'052-211-9934','장생 쟁반 짜장':'052-211-9926'},
        {'땅땅 치킨':'052-212-9934','교촌 치킨':'052-244-9948','굽는쌈닭':'052-246-9993',
         '굽네치킨':'052-245-9995','구어좋은닭':'052-245-9279','기똥찬':'052-245-9281','놀라버린 파닭':'052-212-8895',
         '네네치킨':'052-248-9982','딥스치킨':'052-245-9282','맛있는 파닭':'052-222-9922','맘스치킨':'052-212-9282',
         '맥시칸':'052-212-9990','또래오래':'052-212-9433','멕코이양념통닭':'052-212-9705','BBQ':'052-248-9806',
         'BHC':'052-245-1992','신바람난 파닭':'052-246-5290','신드롬 치킨':'052-245-2292','지코바':'052-211-9989',
         '처갓집 양념 치킨':'052-910-9292','티바 치킨':'052-246-1101','치킨 파티':'052-247-9300','팁스':'052-212-0566',
         '파닭에 미쳐써':'052-244-8898','호식이':'052-243-9289','페리카나':'052-245-2580','올꼬꼬':'052-211-9989',
         '강정이 기가막혀':'052-248-9998','헤롱이':'052-211-1649'},
        {'임실 치즈 피자':'052-243-9900','피자에땅':'052-248-1080','도미노 피자':'052-212-3082','미스터 피자':'052-1577-0077',
         '피자마루':'052-243-8338','BBQ 피자':'052-245-1166','김태호 피자':'052-244-2848'},
        {'장충대가왕족발':'052-224-2777','황지 왕족발순대':'052-245-0089','원할머니 보쌈':'052-245-5281',
         '장충동왕족발보쌈':'052-277-4600'},
        {'돈까스 나라':'052-212-1080','해송 돈까스&롤':'052-211-2118','마쯔리':'052-246-8258','배터지는 생돈까스':'052-211-2360',
         '생생 돈까스':'052-246-9713'}]

TOTAL_FOOD = dict(FOOD[0].items() + FOOD[1].items() + FOOD[2].items() + FOOD[3].items() + FOOD[4].items())

from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()

from selenium import webdriver
br = webdriver.Firefox()

EMOTICON = [":-)",":)","=)",":'-(",":|",":-P",":p","B-)","8-)","XD",":-(",":(",")-:",":/",":-D",":D",";-)",";)","(-;",":-O",":O",":V",":3"]

#from email.MIMEImage import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText

def send_mail(text):
    text = text.decode("unicode-escape").encode("utf-8")
    fromaddr = 'hexa.portal@gmail.com'
    recipients = ['carpedm20@gmail.com']
    toaddrs  = ", ".join(recipients)

    username = ''
    password = ''

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg['Subject'] = text

    part = MIMEText('text', "plain")
    part.set_payload(text)
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, recipients, msg.as_string())
    server.quit()
    print " - mail sended"

def exit_handler():
    """for handle_num in windows:
        print " - Check : " + str(handle_num)

        news[handle_num] = ""

        w = app.window_(handle = handle_num)
        print "[*] END : " + str(w.WindowText()[:20].encode("utf-8"))

        send_message(w, "finish", '', '')
    """
    print "DEAD"

    #send_mail("Bot is DEAD")

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


"""
    elif command in COMMAND['KO_DIC']:
        url = "http://www.google.com/dictionary/json?callback=dict_api.callbacks.id100&q=" + urllib.quote(arg) + "&sl=ko&tl=ko&restrict=pr%2Cde&client=te"

        data = urllib2.urlopen(url)
        data=data.read().replace('\\x','').replace(',200,null)','').replace('dict_api.callbacks.id100(','')

        j = json.loads(data)
        result = ''

        try:
            for idx, d in enumerate(j['webDefinitions'][0]['entries']):
                result += '['+str(idx+1)+'] ' + d['terms'][0]['text'].replace('.;','.\r\n') + '\r\n\r\n'
            result = result[:len(result)-4]
        except:
            result = "찾지 못했습니다 :("""
