import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

data = pd.read_csv('./newexample3.csv')

baseurl = 'https://terms.naver.com'

for i in range(4000, data['link'].size): # data['link'].size
    plusurl = data['link'][i]
    url = baseurl + plusurl
    res = requests.get(url)
    parsing = BeautifulSoup(res.content, 'html.parser')
    print("ㅁㅁ ",i, " ㅁㅁ")
    try:
        contents = parsing.select_one('div.size_ct_v2 img')
        urlretrieve(str(contents['data-src']), "크롤링사진2/"+str(data['id'][i])+".jpg")
    except:
        print(data['이름'][i], "사진 없음")
    