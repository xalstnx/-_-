# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys
import warnings
import pymysql
import json
import os
import urllib.parse
import requests
from flask import Flask, request, jsonify
from functools import wraps
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#경고메시지 숨기기
#warnings.filterwarnings(action='ignore')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def data_chages(data, newmenuarray):
    #조회수 데이터(string형태) 중간에 ','로 나눈후 다시 합친후 int형으로 변환 
    for i in range(data['조회수'].size):
        data['조회수'][i] = data['조회수'][i].split(',')
        data['조회수'][i] = "".join(data['조회수'][i])
        
    #조회수데이터 int형으로 변환
    data['조회수'] = pd.to_numeric(data['조회수'], errors='coerce')
    
    data['재료'] = data['재료'].apply(literal_eval)
    data['건강정보'] = data['건강정보'].apply(literal_eval)
    
    #입력한 재료와 기존의 음식들의 재료를 비교하기 위해 새로운 메뉴(이름:새로운메뉴, 재료:newmenuarray인 하나의 열을 추가함)
    data.loc[data['재료'].size] = ['새로운메뉴', '', '', '', newmenuarray, [], '', '']
    
    #data['재료']에 건강정보까지 합침
    for i in range(data['재료'].size):
        data['재료'][i] = " ".join(data['재료'][i]+data['건강정보'][i])
        #data['건강정보'][i] = " ".join(data['건강정보'][i])
    return data

def get_recommend_racipe_list(df, top=4):
    count_vector = CountVectorizer(ngram_range=(1, 3))
    c_vector_ingredient = count_vector.fit_transform(df['재료'])
    #코사인 유사도를 구한 벡터를 미리 저장
    ingredient_c_sim = cosine_similarity(c_vector_ingredient, c_vector_ingredient).argsort()[:, ::-1]
    # 재료와 건강정보가 일치하는 특정 레시피와 비슷한 레시피를 추천해야 하기 때문에 '특정 레시피' 정보를 뽑아낸다.
    target_recipe_index = df[df['이름'] == '새로운메뉴'].index.values
    #코사인 유사도 중 비슷한 코사인 유사도를 가진 정보를 뽑아낸다.
    sim_index = ingredient_c_sim[target_recipe_index, :top].reshape(-1)
    #본인을 제외
    sim_index = sim_index[sim_index != target_recipe_index].reshape(-1)
    #중복제거
    sim_index = np.asarray(list(set(sim_index)))
    #data frame으로 만들고 조회수로 정렬한 뒤 return
    result = df.iloc[sim_index].sort_values(by='조회수', ascending=False)[:4]

    ''' json형태로 만들기
    df2js = """{
            "이름" : "%s",
            "id" : "%s",
            "대분류" : "%s",
            "소분류" : "%s",
            "재료" : "%s",
            "건강정보" : "%s",
            "조회수" : "%s",
            "link" : "%s"
    }
    """
    js = []
    for item in result.values:
        js.append(json.loads(df2js%tuple(item.tolist())))
    json_data = json.dumps(js, ensure_ascii=False)
    #json_data = json.dumps(new_dict, ensure_ascii=False)
    return json_data
    '''
    # id값만 전달해주는 코드
    outlist = []
    for i in range(result['id'].size):
        outlist.append(result['id'].iloc[i])
    return outlist

@app.route('/startss', methods=['GET'])
def startss():
    newmenu = request.args.get('search')
    strmenu = str(newmenu) 
    newmenuarray = strmenu.split(" ")
    #api사용을 위해 이부분으로 옮김 -> 전처럼 위에서 실행할 경우 첫실행은 잘 작동하지만 두번째부터는 db오류로 오류발생 
    conn = pymysql.connect(host='ip address', port=yourport, user='user name', password='password', db='db name', charset='utf8mb4')
    
    #체크박스로 건강정보를 받기위한 코드
    if(request.args.get('search_cb[]')):
        print("good\n")
        newhealth = request.args.getlist('search_cb[]')
        print(newhealth)
    else:
        print("bad\n")

    #분류별 음식을 추천하기 위해 대분류로 data들을 나누어줌
    returnlist = []
    ##반찬
    query1 = '''select * from newexample3 where 대분류 = '48164' '''
    data1 = pd.read_sql(query1, conn)
    returnlist.append(get_recommend_racipe_list(data_chages(data1, newmenuarray)))
    ###피자/스파게티/스테이크
    query2 = '''select * from newexample3 where 대분류 = '48167' '''
    data2 = pd.read_sql(query2, conn)
    returnlist.append(get_recommend_racipe_list(data_chages(data2, newmenuarray)))
    ###국물요리
    query3 = '''select * from newexample3 where 대분류 = '48163' '''
    data3 = pd.read_sql(query3, conn)
    returnlist.append(get_recommend_racipe_list(data_chages(data3, newmenuarray)))
    ###면류/만두
    query4 = '''select * from newexample3 where 대분류 = '48162' '''
    data4 = pd.read_sql(query4, conn)
    returnlist.append(get_recommend_racipe_list(data_chages(data4, newmenuarray)))
    ###샐러드/수프
    query5 = '''select * from newexample3 where 대분류 = '48166' '''
    data5 = pd.read_sql(query5, conn)
    returnlist.append(get_recommend_racipe_list(data_chages(data5, newmenuarray)))
    ###밥/죽
    query6 = '''select * from newexample3 where 대분류 = '48161' '''
    data6 = pd.read_sql(query6, conn)
    returnlist.append(get_recommend_racipe_list(data_chages(data6, newmenuarray)))

    return str(returnlist)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)