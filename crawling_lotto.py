from bs4 import BeautifulSoup 
from urllib.request import urlopen
from selenium import *
from selenium import webdriver as wd
import time
import pymysql 
import lotto_db

driver = wd.Chrome("C:/chromedriver.exe")
driver.get("http://www.nlotto.co.kr/gameResult.do?method=allWin")

def abc():
    #주소 가져오기
    #url = "http://www.nlotto.co.kr/gameResult.do?method=allWin"
    # html = urlopen(url) 
    html = driver.page_source
    #print(type(html))
    soup = BeautifulSoup(html, 'html.parser')

    #tblType1 mt40 라는 class에 있는 table 전체 가져오기
    table = soup.find('table', {'class':'tblType1 mt40'})
    #print(table)

    #tbody에 있는 내용 가져오기
    body = table.find('tbody')
    #print(body)

    #tr받아서 td정보들을 list로 받기
    data = []
    pdata = []


    for tr in body.findAll('tr'):
        #print(tr)

        if tr.find('td',{'class':'tblType1line1'}) != None :
            continue
        elif tr.find('td',{'class':'tblType1line2'}) != None :
            continue
        else :
            #print("-----------------------")
            tds = list(tr.findAll('td'))
            
            # #tds리스트 안에 있는 정보들 중에 원하는 정보들만 뽑아서 리스트로 만들기

            hoi = tds[0].text
            win_num = tds[1].text
            winner_num = tds[2].text
            win_money = tds[3].text

            url2 = "http://www.nlotto.co.kr/gameResult.do?method=byWin&drwNo=%s" %hoi
            html = urlopen(url2) 
            #print(type(html))
            soup = BeautifulSoup(html, "lxml")

            body = soup.find('h3', {'class' :'result_title'})
        
            span = body.find('span')

            str_date = span.getText()
            str_date = str_date.replace("(","")
            str_date = str_date.replace(")","")
            str_date = str_date.replace("추첨","")
        
            table = soup.find('ul', {'class' : 'fl'})
            body = table.find('span', {'class':'f_blue'})
            total = body.text.replace("원", "").replace(",","")
            #print(total)
                
            url3 = "http://www.nlotto.co.kr/store.do?method=topStore&pageGubun=L645&drwNo=%s" %hoi
            html = urlopen(url3) 
            soup = BeautifulSoup(html, "lxml")

            table = soup.find('table', {'class':'tblType1'})
            body = table.find('tbody')

            for tr2 in body.findAll('tr'):
                if tr2.find('td',{'class':'tblType1line1'}) != None :
                    continue
                elif tr2.find('td',{'class':'tblType1line2'}) != None :
                    continue
                else :
                    tds2 = list(tr2.findAll('td'))
                    name = tds2[1].text
                    loc = tds2[3].text
                    pdata.append([hoi, name, loc])
            
            data.append([hoi, win_num, winner_num, win_money, str_date, total])

    for i in data:
        lotto_db.insert_lotto(i)
        print(i)

    for i in pdata:
        lotto_db.insert_store(i)
        print(i)

page = int(input("enter the last page number :"))

for i in range(1, page+1):
    script = "javascript:selfSubmit('" + str(i) + "')"
    print(script)
    driver.execute_script(script)
    time.sleep(3)    
    abc()   
 
# db table생성
# hoi, win_num, winner_num, win_money, str_date, total, name, loc
# CREATE table lotto(
#    hoi int(10)
#    win_num int(50),
#    winner_num int(10),
#    win_money varchar(50),
#    str_date varchar(50),
#    total varchar(50),
#    primary key(hoi)
# );
