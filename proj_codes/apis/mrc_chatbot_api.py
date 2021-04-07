# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys
import warnings
import pymysql
import json
import os
import urllib.parse
import urllib3
import requests
from flask import Flask, request, jsonify
from functools import wraps
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
from flask_cors import CORS


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

def ETRI_POS_Tagging(text) :
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    accessKey = "your etri key"
    analysisCode = "wsd"
    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": text,
            "analysis_code": analysisCode
        }
    }
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    return Pos_extract(response)
	
	
def Pos_extract(Data) :
    Noun = []
    #print(json.loads(str(Data.data,"utf-8")))
    Extract_a = json.loads(str(Data.data,"utf-8"))['return_object']['sentence']
    for i in range(len(Extract_a)) : 
        Extract_b = dict(Extract_a[i])
        for j in range(len(Extract_b['WSD'])) : 
            if (Extract_b['WSD'][j]['type'] =='NNG' or Extract_b['WSD'][j]['type'] =='NNP'): 
                Noun.append(Extract_b['WSD'][j]['text'])
    return " ".join(Noun)

def get_recommend_list(df, ids, top=1):
    target_recipe_index = df[df['id'] == ids].index.values
    count_vector = CountVectorizer(ngram_range=(0, 2))
    c_vector_ingredient = count_vector.fit_transform(df['keyword'])
    #코사인 유사도를 구한 벡터를 미리 저장
    ingredient_c_sim = cosine_similarity(c_vector_ingredient, c_vector_ingredient)
    print(ingredient_c_sim)
    ingredient_c_sim_change = ingredient_c_sim.argsort()[:, int(target_recipe_index)-1::-1]
    print(ingredient_c_sim_change)
    # 재료와 건강정보가 일치하는 특정 레시피와 비슷한 레시피를 추천해야 하기 때문에 '특정 레시피' 정보를 뽑아낸다.

    #코사인 유사도 중 비슷한 코사인 유사도를 가진 정보를 뽑아낸다.
    print("\n#################   ", ingredient_c_sim[target_recipe_index][0][ingredient_c_sim_change[target_recipe_index][0][0]],"   ##################\n")
    cc_sim_high = ingredient_c_sim[target_recipe_index][0][ingredient_c_sim_change[target_recipe_index][0][0]]
    sim_index = ingredient_c_sim_change[target_recipe_index, :top].reshape(-1)
    #본인을 제외
    sim_index = sim_index[sim_index != target_recipe_index].reshape(-1)
    #data frame으로 만들고 조회수로 정렬한 뒤 return
    result = df.iloc[sim_index]
    returnarray = []
    returnarray.append(result['paragraph'])
    returnarray.append(cc_sim_high)
    return returnarray

@app.route('/chats', methods=['GET'])
def chats():
    data = pd.read_csv('./ingre6.csv')
    mrcorwiki = 0 # 0 = 기계독해 api / 1 = 위키백과 api
    c_sim_high = 0.0
    question = request.args.get('question')
    data.loc[data['keyword'].size] = ['newitem', ETRI_POS_Tagging(question), '']
    recomarray = get_recommend_list(data, 'newitem')
    passage = str(recomarray[0].values)
    accessKey = "your etri key"
    c_sim_high = float(recomarray[1])
    
    print('\n@@@@',c_sim_high,'@@@@\n')
    
    if(c_sim_high >= 0.9):
        print("0.9이상이여서 db에서 찾음.")
        mrcorwiki = 0
        openApiURL = "http://aiopen.etri.re.kr:8000/MRCServlet"
        requestJson = {
        "access_key": accessKey,
            "argument": {
                "question": question,
                "passage": passage
            }
        }
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)
        )

    else:
        print("0.9미만이여서 위키에서 찾음.")
        mrcorwiki = 1
        openApiURL = "http://aiopen.etri.re.kr:8000/WikiQA"
        type = "hybridqa"
        requestJson = {
        "access_key": accessKey,
        "argument": {
            "question": question,
            "type": type
        }
        }
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)
        )

    print("[responseCode] " + str(response.status))
    print("[responBody]")
    jdata = json.loads(response.data)
    if mrcorwiki == 0:
        print(jdata["return_object"]["MRCInfo"]["answer"])
        return str(jdata["return_object"]["MRCInfo"]["answer"])
    else:
        print(jdata["return_object"]["WiKiInfo"]["AnswerInfo"])
        if jdata["return_object"]["WiKiInfo"]["AnswerInfo"] == []:
            print(jdata)
            return str("위키에서 답을 찾을 수 없음.")
        else:
            print(jdata["return_object"]["WiKiInfo"]["AnswerInfo"][0]["answer"])
            return str(jdata["return_object"]["WiKiInfo"]["AnswerInfo"][0]["answer"])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5002)