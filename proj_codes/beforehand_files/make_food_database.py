import requests

from bs4 import BeautifulSoup

import re

import csv

###############################################################################
#항암효과가 있는 재료들
anti_cancer = ['순무', '씀바귀', '우엉', '파프리카', '브로콜리', '가지', '표고버섯', '살구', '포도', '쪽파', '흑미',
               '토마토', '헤즐넛', '매실', '도라지', '고구마', '보리순', '고추', '김치', '아마씨', '아로니아', '렌틸콩',
               '검은콩', '서리태', '송이버섯', '청각', '콩', '쑥', '마늘', '깻잎', '당근', '빨간파프리카', '주황파프리카',
               '꽃송이버섯', '버섯', '고등어', '꽁치', '정어리', '방어', '연어', '삼치', '참치', '청어', '전갱이', '차가버섯', 
               '냉이', '단호박', '부추', '흑임자', '검은깨', '콜리플라워', '시금치', '팽이버섯', '배추', '양배추', '동충하초']
#고혈압에 효과가 있는 재료들
high_blood_pressure = ['오만둥이', '마늘', '메밀', '양송이버섯', '여주', '올리브', '양파', '연근', '녹두', '더덕',
                       '토마토', '고구마', '강낭콩', '연어', '바나나', '아몬드', '호박씨', '목이버섯', '비트', '송이버섯',
                       '가지', '감자', '파프리카', '브로콜리', '당근', '피망', '참나물', '고들빼기', '팥', '하수오', '쑥갓',
                       '호두', '붉은팥', '전복', '미나리', '꽈리고추']
#당뇨에 효과가 있는 재료들
diabetes = ['여주', '녹두', '더덕', '토마토', '강낭콩', '아몬드', '체리', '아보카도', '율무', '돼지감자', '두릅', '백복령', '뽕잎', 
            '함초', '흑임자', '검은깨', '사과', '마']

#관절염에 효과가 있는 재료들
arthritis = ['다슬기', '도라지', '오가피', '꼼장어', '마늘', '우유', '연어','가시오가피', '피망', '멸치', '차가버섯',
             '미역', '마른미역', '두부', '브로콜리', '다시마', '건포도', '아욱', '매생이', '톳']

###############################################################################
# 재료리스트에 있는 재료들이 어떤 건강정보에 해당하는지 판별
def decidehealthingredients(ingredients):
    foodhealthdata = []
    if (set(ingredients)&set(anti_cancer)):
        foodhealthdata.append('항암')
    if (set(ingredients)&set(high_blood_pressure)):
        foodhealthdata.append('고혈압')
    if (set(ingredients)&set(diabetes)):
        foodhealthdata.append('당뇨')
    if (set(ingredients)&set(arthritis)):
        foodhealthdata.append('관절염')
    return foodhealthdata

###############################################################################

def list_ingredient(url):   # 재료를 찾아 리스트로 반환하는 함수
    
    torf = False      # h3섹션에 재료가 없으면 torf를 false로 유지해 h4섹션에서 재료 탐색
    foodbaseurl = 'https://terms.naver.com'
    ingredienturl = foodbaseurl + str(url)
    res = requests.get(ingredienturl)
    
    parsing = BeautifulSoup(res.content, 'html.parser')
    
    titles = parsing.find_all('h3', 'stress')
    
    for title in titles:
        #print(title.text)
        if "재료" in title.text:
            data = title.find_next().text
            torf = True
            break
        
    if torf == False:
        titles = parsing.find_all('h4')
        
        for title in titles:
            if "재료" in title.text:
                data = title.find_next().text
                
    
    try:
        #print(data)        
                
        t_data = re.findall('( [가-힣 ]+ | [가-힣]+\(|[가-힣]+[0-9]\) |^[가-힣]+ )', data)  #재료이름만 리스트에 저장
        
        #print(t_data)
        
        for i in range(len(t_data)):  #리스트안에 "재료"가 포함된 단어가 있을경우 제거
            try:
                if "재료" in t_data[i]:
                    del t_data[i]
            except:   #제거 된경우 리스트의 수가 줄어들어 out of range 오류가 떠 오류처리
                #print("out of range")
                continue
        
        for i in range(len(t_data)):    #공백, 숫자, 영어, 기호 제거
            patterns = re.compile('[^가-힣]| ')
            t_data[i] = re.sub(patterns, '', t_data[i])
            
        t_data = list(set(t_data))  #리스트안 중복된 값 제거
        
        #print(t_data)
        return t_data
        
    except NameError:   #리스트에 재료가 없을경우
        print("no data")

###############################################################################

def makefooddatabase(pagebaseurl, lastpagenum, aorw):
    if aorw == "w":     
        print("새로쓰기 모드로 작성")
        f = open('test2.csv', 'w', encoding='utf-8', newline='')   #두번째를 'a'로 하면 이어쓰기, 'w'로 하면 새로 쓰기
        csvwriter = csv.writer(f)
        csvwriter.writerow(['이름', 'id', '대분류', '소분류', '재료', '건강정보', '조회수', 'link'])    #데이터베이스 첫줄
    elif aorw == "a":
        print("이어쓰기 모드로 작성")
        f = open('test2.csv', 'a', encoding='utf-8', newline='')
        csvwriter = csv.writer(f)
    
    for pagenum in range(1, lastpagenum):     # 페이지 수 지정 1페이지~(lastpagenum-1)페이지까지
        url = pagebaseurl + str(pagenum)
        print(url)
        res = requests.get(url)
        parsing = BeautifulSoup(res.content, 'html.parser')
        
        titles = parsing.select('div.info_area')
        
        searchlist = []
    
        for ttitle in titles:
            temp = []       # temp = 한 음식 row 리스트의 집합
            title = ttitle.strong.a
            view = ttitle.find('em', {'class' : 'count'})
            newtitlelist = re.findall('[가-힣 ]+', title.text)  #이름에서 한글만 가져
            newtitle = ''
            itemurl = title.attrs['href']
            ingredients = list_ingredient(itemurl)  #재료 리스트 가져오는 함수
            if ingredients == None or len(ingredients)==0:  #재료 리스트에 아무것도 없으면 추가하지 않음
                continue
            else:
                for names in newtitlelist:
                    newtitle = newtitle + names
                newtitle = re.sub('만드는 법', '', newtitle)  # 이름에서 "만드는 법" 제거
                newtitle = newtitle.strip()                  #문자열 앞,뒤 공백제거
                temp.append(newtitle)
                foodid = re.findall('[0-9]+', itemurl)  # url에서 음식id, 분류id 찾아서 리스트에 저장
                temp.append(foodid[0])  #음식 id
                temp.append(foodid[1])  #대분류 ex) 반찬
                temp.append(foodid[2])  #소분류 ex) 구이
                temp.append(ingredients)
                foodhealthlist = decidehealthingredients(ingredients)
                temp.append(foodhealthlist)
                temp.append(view.text)
                temp.append(itemurl)
                searchlist.append(temp)
                #print(title.attrs['href'])
                #print(title.text)
                
        for i in searchlist:
            csvwriter.writerow(i)
    
    f.close()

###############################################################################
"""
##모든 식재료 리스트 csv만들기
def makeallingredientdatabase(pagebaseurl, lastpagenum):
    print("새로쓰기 모드로 작성")
    f = open('allingredients.csv', 'w', encoding='ms949', newline='')
    csvwriter = csv.writer(f)
    ingredientlist = []
    for pagenum in range(1, lastpagenum):
        url = pagebaseurl + str(pagenum)
        print(url)
        res = requests.get(url)
        parsing = BeautifulSoup(res.content, 'html.parser')
        titles = parsing.select('div.info_area > div.subject > strong > a:nth-child(1)')
        
        for title in titles:
            itemurl = title.attrs['href']
            ingredients = list_ingredient(itemurl)
            if ingredients == None or len(ingredients)==0:  #재료 리스트에 아무것도 없으면 추가하지 않음
                continue
            else:
                for ingredient in ingredients:
                    ingredientlist.append(ingredient)
            
    ingredientlist = list(set(ingredientlist))
    csvwriter.writerow(ingredientlist)
    f.close()
    print(ingredientlist)
"""
###############################################################################
#반찬

makefooddatabase('https://terms.naver.com/list.nhn?cid=48164&categoryId=48202&page=', 32, 'w')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48164&categoryId=48203&page=', 22, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48164&categoryId=48204&page=', 40, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48164&categoryId=48205&page=', 33, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48164&categoryId=48206&page=', 21, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48164&categoryId=48207&page=', 20, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48164&categoryId=48208&page=', 30, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48164&categoryId=48209&page=', 6, 'a')
###############################################################################
#피자/스파게티/스테이크
makefooddatabase('https://terms.naver.com/list.nhn?cid=48167&categoryId=48216&page=', 3, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48167&categoryId=48217&page=', 8, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48167&categoryId=48218&page=', 5, 'a')
###############################################################################
#국물요리
makefooddatabase('https://terms.naver.com/list.nhn?cid=48163&categoryId=48200&page=', 49, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48163&categoryId=48201&page=', 24, 'a')
###############################################################################
#면류/만두
makefooddatabase('https://terms.naver.com/list.nhn?cid=48162&categoryId=48198&page=', 21, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48162&categoryId=48199&page=', 5, 'a')
###############################################################################
#샐러드/수프
makefooddatabase('https://terms.naver.com/list.nhn?cid=48166&categoryId=48214&page=', 17, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48166&categoryId=48215&page=', 9, 'a')
###############################################################################
#밥/죽
makefooddatabase('https://terms.naver.com/list.nhn?cid=48161&categoryId=48196&page=', 47, 'a')
makefooddatabase('https://terms.naver.com/list.nhn?cid=48161&categoryId=48197&page=', 16, 'a')
###############################################################################
