import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from urllib.error import HTTPError
from urllib.error import URLError
import csv


def list_ingredient():
    print("새로쓰기 모드로 작성")
    f = open('ingre3.csv', 'w', encoding='utf-8-sig', newline='')
    csvwriter = csv.writer(f)
    csvwriter.writerow(['id', 'keyword', 'paragraph'])
    foodbaseurl = 'https://www.kamis.or.kr/customer/archive/archive.do?action=detail&archiveNo=' #1~221
    rowlist = []
    start_num = int(input("시작값입력(1~221)"))
    end_num = int(input("마지막값입력(1~221)"))
    current_num = start_num
    for num in range(start_num, end_num+1):
        ingredienturl = foodbaseurl + str(num)
        res = requests.get(ingredienturl)
        parsing = BeautifulSoup(res.content, 'html.parser')
        parsing2 = BeautifulSoup(res.content, 'html.parser')
        try:
            new_page = urlopen(ingredienturl)
            all_text = ''
        
            fname = parsing.find('div', {'class':'tbl_prdesc'}).find('dl').select_one('dt')
            target_text_without_child_tags = [
                onlyname
                for onlyname
                in fname
                if isinstance(onlyname, NavigableString)
            ]
            realname = "".join(target_text_without_child_tags)
            
            tables = parsing2.find('div', {'class':'tbl_comn scroll_none'}).find_all('table')
            for table in tables:
                trs = table.find_all('tr')
                for tr in trs:
                    if tr.find('td') != None and tr.find('th') != None:
                        th = tr.find('th').get_text(strip=True)
                        td = tr.find('td').get_text(strip=True)
                        all_text += (th + " : " + td + ". ")
                if all_text != '':
                    break
                
            temp = []
            temp.append(current_num)
            temp.append(realname)
            temp.append(all_text)
            rowlist.append(temp)
            print("done - ",current_num, num, realname)
            current_num+=1
        except HTTPError as e:
            print(num, e)
        except URLError as e:
            print(num, e)
            
    for i in rowlist:
        csvwriter.writerow(i)

list_ingredient()
